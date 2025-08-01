import json
from web.services.run_playwright_script import run_playwright_script

def test_extrair_link_esus():
    config = [
        {
            "action": "goto",
            "url": "https://sisaps.saude.gov.br/sistemas/esusaps/"
        },
        {
            "action": "wait_for_selector",
            "selector": "[class*='downloadButton_']"
        },
        {
            "action": "extract_text",
            "selector": "[class*='downloadButton_']",
            "store_as": "versao_label",
            "regex": "\\d+\\.\\d+\\.\\d+"
        },
        {
            "action": "click",
            "selector": "[class*='downloadButton_']"
        },
        {
            "action": "wait_for_selector",
            "selector": "a"
        },
        {
            "action": "find_and_click_link",
            "text_contains": "Leia Mais",
            "aria_label_contains_variable": "versao_label"
        },
        {
            "action": "wait_for_selector",
            "selector": "button:has-text(\"para Linux\")"
        },
        {
            "action": "capture_current_url",
            "store_as": "url_release_page"
        },
        {
            "action": "find_and_extract_download_link",
            "text_contains": ["Versão para Linux", "Download para Linux"],
            "store_as": "link_linux"
        }
    ]

    status, output = run_playwright_script(config)

    print("Status:", status)
    print("Resultado:", output)

    assert status == "success", "Falha ao extrair dados com Playwright"
    
    # se output for JSON serializado:
    data = json.loads(output) if isinstance(output, str) and output.startswith("{") else {}
    assert "link_linux" in data
    assert data["link_linux"].endswith(".jar")
