import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    options = Options()
    options.add_argument('--start-maximized')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def limpar_preco(texto_preco, valor_numerico=None):
    if valor_numerico is not None:
        return float(valor_numerico) / 100

    if not texto_preco: return 0.0
    
    texto_lower = texto_preco.lower()
    if "gratuito" in texto_lower or "free" in texto_lower or "jogar" in texto_lower:
        return 0.0
        
    try:
        limpo = texto_preco.replace('R$', '').replace(' ', '').replace('.', '').replace(',', '.')
        match = re.search(r'(\d+\.?\d*)', limpo)
        if match:
            return float(match.group(1))
        return 0.0
    except ValueError:
        return 0.0

class SteamScraper:
    def buscar(self, driver, jogo):
        print(f"🔄 Buscando '{jogo}' na Steam...")
        try:
            driver.get(f"https://store.steampowered.com/search/?term={jogo.replace(' ', '+')}")
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.ID, "search_resultsRows")))
            
            primeiro_jogo = driver.find_element(By.CSS_SELECTOR, "a.search_result_row")
            titulo = primeiro_jogo.find_element(By.CLASS_NAME, "title").text
            
            try:
                div_preco = primeiro_jogo.find_element(By.CSS_SELECTOR, ".search_price_discount_combined")
                preco_centavos = div_preco.get_attribute("data-price-final")
                
                if preco_centavos:
                    preco_valor = limpar_preco("", valor_numerico=preco_centavos)
                    texto_preco = f"R$ {preco_valor:.2f}".replace('.', ',')
                else:
                    texto_preco = div_preco.text
                    preco_valor = 0.0
            except:
                texto_preco = primeiro_jogo.find_element(By.CLASS_NAME, "search_price").text
                preco_valor = limpar_preco(texto_preco)

            return {
                "loja": "Steam",
                "titulo": titulo,
                "preco_texto": texto_preco.strip().replace('\n', ' '),
                "preco_valor": preco_valor,
                "url": primeiro_jogo.get_attribute("href")
            }
        except Exception as e:
            print(f"❌ Erro na Steam: {e}")
            return None

class EpicScraper:
    def buscar(self, driver, jogo):
        print(f"🔄 Buscando '{jogo}' na Epic Games...")
        try:
            driver.get(f"https://store.epicgames.com/pt-BR/browse?q={jogo.replace(' ', '%20')}&sortBy=relevancy")
            wait = WebDriverWait(driver, 15)

            wait.until(EC.presence_of_element_located((By.TAG_NAME, "section")))
            time.sleep(5)

            xpath_busca = f"//a[contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{jogo.lower()}')]"
            
            try:
                card = driver.find_element(By.XPATH, f"({xpath_busca})[1]")
            except:
                try:
                    card = driver.find_element(By.CSS_SELECTOR, "section ul li a")
                except:
                    return None

            titulo = card.get_attribute("aria-label")
            if not titulo:
                titulo = jogo.capitalize()

            texto_completo = card.get_attribute("innerText")
            texto_preco = "R$ 0,00"
            
            if "Gratuito" in texto_completo or "Free" in texto_completo:
                texto_preco = "Gratuito"
            else:
                encontrados = re.findall(r'R\$\s*[\d\.]+,?\d*', texto_completo)
                
                if encontrados:
                    texto_preco = encontrados[-1]
                elif "Ver ofertas" in texto_completo or "View offers" in texto_completo:
                    texto_preco = "Ver Ofertas (Várias Edições)"
                    match_apartir = re.search(r'[\d\.]+,?\d*', texto_completo)
                    if match_apartir:
                        texto_preco = f"A partir de R$ {match_apartir.group(0)}"

            return {
                "loja": "Epic Games",
                "titulo": titulo,
                "preco_texto": texto_preco,
                "preco_valor": limpar_preco(texto_preco),
                "url": driver.current_url
            }
        except Exception as e:
            print(f"❌ Erro na Epic Games: {str(e)[:100]}...")
            return None

def main():
    print("🚀 Iniciando GamePriceWars...")
    driver = setup_driver()
    
    try:
        nome_jogo = input("\n🎮 Digite o nome do jogo: ").strip()
        resultados = []

        steam = SteamScraper()
        res_steam = steam.buscar(driver, nome_jogo)
        if res_steam: resultados.append(res_steam)

        epic = EpicScraper()
        res_epic = epic.buscar(driver, nome_jogo)
        if res_epic: resultados.append(res_epic)

        print("\n" + "="*50)
        print(f"RELATÓRIO DE PREÇOS: {nome_jogo.upper()}")
        print("="*50)

        melhor_opcao = None
        menor_preco = float('inf')

        if not resultados:
            print("⚠️ Nenhum jogo encontrado. Tente outro nome.")
        else:
            for res in resultados:
                print(f"📍 {res['loja']}: {res['titulo']}")
                print(f"   Preço: {res['preco_texto']}")
                print("-" * 30)
                
                if res['preco_valor'] is not None and res['preco_valor'] < menor_preco and res['preco_valor'] > 0:
                    menor_preco = res['preco_valor']
                    melhor_opcao = res
                elif res['preco_valor'] == 0 and "Gratuito" in res['preco_texto']:
                     menor_preco = 0
                     melhor_opcao = res

            print("="*50)
            if melhor_opcao:
                status = "GRÁTIS!" if melhor_opcao['preco_valor'] == 0 else f"R$ {melhor_opcao['preco_valor']:.2f}"
                print(f"🏆 MELHOR OFERTA: {melhor_opcao['loja']} ({status})")
            
            pasta_prints = "screenshots"
            if not os.path.exists(pasta_prints):
                os.makedirs(pasta_prints)

            nome_arquivo = f"resultado_{nome_jogo.replace(' ', '_')}.png"
            caminho_completo = os.path.join(pasta_prints, nome_arquivo)
            
            driver.save_screenshot(caminho_completo)
            print(f"\n📸 Evidência salva em: {caminho_completo}")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()