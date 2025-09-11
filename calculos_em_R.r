# install.packages(c("httr", "jsonlite", "dplyr", "ggplot2"))

library(httr)
library(jsonlite)
library(dplyr)
library(ggplot2)

tryCatch({
  df <- read.csv("dados_fazenda.csv")
  print("Dados da fazenda carregados com sucesso do arquivo CSV!")
}, error = function(e) {
  stop("ERRO: O arquivo 'dados_fazenda.csv' não foi encontrado. Por favor, execute o programa Python e use a opção '5' para exportar os dados antes de rodar este script.")
})

lat <- -8.31583
lon <- -36.29278
api_key <- "d15e6bd014a6b5a87a2b7b55a9dec8c0" 

url <- paste0("https://api.openweathermap.org/data/2.5/weather?",
              "lat=", lat, "&lon=", lon,
              "&units=metric&lang=pt_br&appid=", api_key)

clima_info <- NULL
tryCatch({
  res <- GET(url)
  if (status_code(res) == 200) {
    dados_clima <- fromJSON(content(res, "text"))
    
    clima_info <- data.frame(
      Local = "Tacaimbó-PE",
      Temperatura = dados_clima$main$temp,
      Umidade = dados_clima$main$humidity,
      Condicao = dados_clima$weather$description[1]
    )
    
    print("Dados de clima obtidos com sucesso:")
    print(clima_info)
    
  } else {
    print(paste("Aviso: Não foi possível obter os dados de clima. Código:", status_code(res)))
  }
}, error = function(e) {
  print(paste("Aviso: Ocorreu um erro na chamada da API de clima:", e$message))
})

if (!is.null(clima_info)) {
  df$Temperatura <- clima_info$Temperatura
  df$Umidade <- clima_info$Umidade
} else {
  df$Temperatura <- NA
  df$Umidade <- NA
}

df_summary <- df %>%
  group_by(Cultura) %>%
  summarise(
    Area_media = mean(Area_ha),
    Insumo_medio = mean(Quantidade_L),
    Temp_media = mean(Temperatura, na.rm = TRUE),
    Umid_media = mean(Umidade, na.rm = TRUE),
    # Adicionei aqui a parte do Desvio - Cauã
    Area_desvio_padrao_ha = sd(Area_ha),
    Insumo_desvio_padrao_L = sd(Quantidade_L)
  )

print("Resumo Estatístico por Cultura")
print(df_summary)

ggplot(df_summary, aes(x = Cultura, y = Insumo_medio, fill = Cultura)) +
  geom_col() +
  geom_errorbar(
    aes(ymin = Insumo_medio - Insumo_desvio_padrao_L, 
        ymax = Insumo_medio + Insumo_desvio_padrao_L),
    width = 0.2
  ) +
  geom_text(aes(label = paste0("Temp: ", round(Temp_media, 1), "°C")), vjust = -1.5) +
  labs(
    title = "Insumo médio (L) por Cultura vs Temperatura em Tacaimbó-PE",
    subtitle = "As barras de erro representam o desvio padrão do insumo",
    x = "Cultura",
    y = "Quantidade média de insumo (L)"
  ) +
  theme_minimal()

