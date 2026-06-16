import os
import time
import uuid
import requests
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from fastmcp import FastMCP
from loguru import logger
from google import genai

# Load environment variables
load_dotenv(override=True)

# Initialize FastMCP
mcp = FastMCP("Sub-cheap-McpAiAgent")

# Configure logger
logger.remove()
logger.add("mcp_server.log", rotation="10 MB", retention=2, serialize=True, level="DEBUG")
logger.add("error.log", rotation="10 MB", retention=2, serialize=True, level="ERROR")


# Sub-LLM Clients
class SubLLMClient:
    @staticmethod
    def call_gemini(prompt: str) -> str:
        api_key = os.getenv("GOOGLE_API_KEY")
        model_name = os.getenv(
            "GEMINI_MODEL", "gemini-2.5-flash"
        )  # Updated default model name for genai
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set in .env")

        client = genai.Client(api_key=api_key)

        logger.info(f"Calling Gemini ({model_name})...")
        try:
            start_time = time.perf_counter()
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=0.2,
                ),
            )
            elapsed = time.perf_counter() - start_time
            logger.info(f"Gemini call completed in {elapsed:.2f}s")
            return response.text.strip()
        except Exception:
            logger.exception("Gemini call failed")
            raise

    @staticmethod
    def call_ollama(prompt: str) -> str:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        model_name = os.getenv("OLLAMA_MODEL", "gemma2:9b")

        logger.info(f"Calling Ollama ({model_name})...")
        try:
            start_time = time.perf_counter()
            response = requests.post(
                f"{base_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2},
                },
                timeout=60,
            )
            response.raise_for_status()
            elapsed = time.perf_counter() - start_time
            logger.info(f"Ollama call completed in {elapsed:.2f}s")
            return response.json().get("response", "").strip()
        except Exception:
            logger.exception("Ollama call failed")
            raise


def clean_code_output(text: str) -> str:
    """Removes markdown code blocks if present."""
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        return "\n".join(lines).strip()
    return text.strip()


@mcp.tool()
def draft_code(
    path: str,
    instruction: str,
    start_line: Optional[int] = None,
    end_line: Optional[int] = None,
    reference_context: Optional[str] = None,
    model: Optional[str] = None,
) -> str:
    """
    Drafts or modifies code using an inexpensive sub-LLM.

    Args:
        path: Target file path.
        instruction: What to do with the code.
        start_line: 1-indexed start line for editing (inclusive).
        end_line: 1-indexed end line for editing (inclusive).
        reference_context: Additional code or info for the sub-LLM.
        model: 'gemini' or 'ollama'. Defaults to DEFAULT_MODEL in .env.
    """
    run_id = str(uuid.uuid4())
    start_total_time = time.perf_counter()

    with logger.contextualize(run_id=run_id):
        logger.info(f"Started draft_code for path: {path}")
        try:
            if start_line is not None and end_line is not None:
                if start_line > end_line:
                    return "Error: start_line cannot be greater than end_line."

            file_path = Path(path)
            target_snippet = ""
            full_content = []

            # 1. Read existing file if it exists
            if file_path.exists():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        full_content = f.readlines()

                    if start_line is not None and end_line is not None:
                        # Extract specific range (1-indexed)
                        s_idx = max(0, start_line - 1)
                        e_idx = min(len(full_content), end_line)
                        target_snippet = "".join(full_content[s_idx:e_idx])
                        logger.debug(f"Extracted lines {start_line}-{end_line} from {path}")
                    else:
                        target_snippet = "".join(full_content)
                        logger.debug(f"Read full content from {path}")
                except Exception as e:
                    logger.exception("Failed to read existing file")
                    return f"Error reading file: {e}"
            else:
                logger.debug(f"File {path} does not exist. Starting with empty snippet.")

            # 2. Build Prompt
            system_prompt = (
                "You are a professional code factory. Your task is to modify or write code based on instructions.\n"
                "RULES:\n"
                "- Output ONLY the code. No explanations, no markdown blocks, no 'Here is your code'.\n"
                "- Maintain the existing indentation and style.\n"
                "- If modifying a snippet, provide the FULL replacement for that snippet.\n"
            )

            user_prompt = f"### Instruction:\n{instruction}\n\n"
            if target_snippet:
                user_prompt += f"### Current Code Snippet:\n{target_snippet}\n\n"
            if reference_context:
                user_prompt += f"### Reference Context:\n{reference_context}\n\n"

            final_prompt = f"{system_prompt}\n{user_prompt}"

            # 3. Call Sub-LLM
            selected_model = model or os.getenv("DEFAULT_MODEL", "gemini")
            try:
                if selected_model == "gemini":
                    generated_code = SubLLMClient.call_gemini(final_prompt)
                else:
                    generated_code = SubLLMClient.call_ollama(final_prompt)

                generated_code = clean_code_output(generated_code)
            except Exception as e:
                logger.exception("Sub-LLM generation failed")
                return f"Sub-LLM call failed: {e}"

            # 4. Write back to file
            try:
                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)

                if start_line is not None and end_line is not None and full_content:
                    # Line-based merge
                    s_idx = max(0, start_line - 1)
                    e_idx = min(len(full_content), end_line)

                    # Prepare new lines
                    new_lines = generated_code.splitlines(keepends=True)
                    # Ensure the last line has a newline if the original snippet did
                    if generated_code and not generated_code.endswith("\n"):
                        new_lines[-1] += "\n"

                    updated_content = full_content[:s_idx] + new_lines + full_content[e_idx:]

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.writelines(updated_content)

                    msg = f"✅ Updated lines {start_line}-{end_line} in '{path}' using {selected_model}."
                else:
                    # Full write / Overwrite
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(
                            generated_code + ("\n" if not generated_code.endswith("\n") else "")
                        )

                    msg = f"✅ Successfully wrote to '{path}' using {selected_model}."

                total_elapsed = time.perf_counter() - start_total_time
                logger.info(f"{msg} (Total time: {total_elapsed:.2f}s)")
                return msg

            except Exception as e:
                logger.exception("Failed to write file")
                return f"Error writing file: {e}"

        except Exception as e:
            logger.exception("Unexpected fatal error in draft_code")
            return f"Fatal error: {e}"


if __name__ == "__main__":
    try:
        mcp.run()
    except Exception:
        logger.exception("MCP Server crashed")
        input("Press Enter to exit...")
