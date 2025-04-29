from web.services.run_playwright_script import run_playwright_script


def test_captura_versao_ibirataia():
    task_config = [
        {"action": "goto", "url": "https://ibirataia.esus.noharm.ai/"},
        {
            "action": "wait_for_selector",
            "selector": "button[data-cy='LoginForm.access-button']",
        },
        {
            "action": "extract_text",
            "selector": "span:has-text('Versão')",
            "regex": "\\d+\\.\\d+\\.\\d+",
            "store_as": "versao",
        },
    ]

    status, output = run_playwright_script(task_config)

    print(f"Status: {status}")
    print(f"Output: {output}")

    if status == "success":
        assert "versao" in output, "Deveria ter capturado a versão"
        assert isinstance(output["versao"], str), "Versão deve ser uma string"
        assert output["versao"].count(".") == 2, "Versão deve ter dois pontos"
    else:
        assert "error" in output, "Erro deveria estar no output"
        assert "message" in output, "Mensagem de erro deveria estar no output"
