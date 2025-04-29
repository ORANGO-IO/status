from playwright.sync_api import sync_playwright
import re

def format_playwright_error(error: Exception) -> dict:
    """
    Formata erros do Playwright para um dicionário JSON simples.

    Args:
        error (Exception): Exceção capturada durante execução Playwright.

    Returns:
        dict: Estrutura compacta com erro e mensagem.
    """
    return {
        "error": "playwright action failed",
        "message": str(error).strip()
    }

def run_playwright_script(task_config: list) -> tuple:
    context = {}
    extracted_result = None

    print("▶️ Iniciando execução do script Playwright...")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            for step in task_config:
                action = step.get("action")
                print(f"👉 Executando ação: {action}")

                try:
                    if action == "goto":
                        print(f"🌐 Acessando URL: {step['url']}")
                        page.goto(step["url"], timeout=30000)

                    elif action == "wait_for_selector":
                        print(f"⏳ Aguardando seletor: {step['selector']}")
                        page.wait_for_selector(step["selector"], timeout=10000)

                    elif action == "extract_text":
                        text = page.inner_text(step["selector"])
                        if step.get("regex"):
                            matches = re.findall(step["regex"], text)
                            text = matches[0] if matches else text
                            print(f"🔍 Versão extraída com regex: {text}")
                        else:
                            print(f"📦 Texto extraído: {text}")

                        if "store_as" in step:
                            context[step["store_as"]] = text
                        else:
                            extracted_result = text

                    elif action == "click":
                        print(f"🖱️ Clicando em: {step['selector']}")
                        page.click(step["selector"])

                    elif action == "find_and_click_link":
                        versao = context.get(step["aria_label_contains_variable"])
                        print(f"🔍 Buscando link com 'Leia Mais' e aria-label contendo: {versao}")
                        links = page.query_selector_all("a")
                        for link in links:
                            inner = link.inner_text()
                            aria = link.get_attribute("aria-label") or ""
                            if step["text_contains"] in inner and versao in aria:
                                print(f"✅ Link encontrado: {inner} — {aria}")
                                link.click()
                                break

                    elif action == "find_and_extract_download_link":
                        print("🔍 Buscando botão com texto:", step["text_contains"])
                        buttons = page.query_selector_all("button")
                        for btn in buttons:
                            inner = btn.inner_text()
                            if step["text_contains"] in inner:
                                with page.expect_download() as download_info:
                                    btn.click()
                                download = download_info.value
                                url = download.url
                                print(f"📥 URL de download capturado: {url}")
                                if "store_as" in step:
                                    context[step["store_as"]] = url
                                else:
                                    extracted_result = url
                                break

                    elif action == "capture_current_url":
                        url = page.url
                        print(f"🌐 URL atual capturada: {url}")
                        if "store_as" in step:
                            context[step["store_as"]] = url
                        else:
                            extracted_result = url

                except Exception as e:
                    print(f"❌ Erro durante '{action}':", e)
                    return "error", format_playwright_error(e)

            browser.close()
            print("✅ Execução finalizada")

        # Decide o que retornar
        return "success", extracted_result or context

    except Exception as e:
        print("❌ Erro fatal no Playwright:", e)
        return "error", format_playwright_error(e)