# R script: AI TB CXR HTA – literature processing
library(tidyverse)
refs <- read_csv("data/ai_tb_cxr_search_results.csv")
refs_clean <- refs %>% distinct(title, .keep_all = TRUE)
write_csv(refs_clean, "output/ai_tb_cxr_screening_sheet.csv")
