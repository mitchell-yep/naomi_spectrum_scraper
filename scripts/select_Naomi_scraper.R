library(tidyverse)
library(jsonlite)
library(svDialogs)

base_url <- "https://naomiviewerserver.azurewebsites.net/api/v1/data?"

# Country codes
countries = c('AGO', 'BDI', 'BEN', 'BFA', 'BWA', 'CAF', 'CMR', 'COD', 'COG', 'CIV',
             'ETH', 'GAB', 'GHA', 'GIN', 'GMB', 'GNB', 'KEN', 'LBR', 'LSO','MWI', 'MLI',
             'MOZ', 'NAM', 'NER', 'RWA', 'SEN', 'SLE', 'SWZ', 'TCD', 'TGO', 'UGA',
             'ZMB', 'ZWE','HIT', 'STP', 'TZA', 'ERI', 'NGA', 'ZAF')

names = c('Angola', 'Burundi', 'Benin', 'Burkina Faso', 'Botswana', 'Central African Republic',
         'Cameroon', 'Democratic Republic of the Congo', 'Republic of the Congo', "Ivory Coast (Côte d'Ivoire)",
         'Ethiopia', 'Gabon', 'Ghana', 'Guinea', 'The Gambia', 'Guinea-Bissau', 'Kenya', 'Liberia', 'Lesotho','Malawi', 'Mali',
         'Mozambique', 'Namibia', 'Niger', 'Rwanda', 'Senegal', 'Sierra Leone', 'Eswatini', 'Chad',
         'Togo', 'Uganda', 'Zambia', 'Zimbabwe', 'Haiti', 'Sao Tome and Principe', 'Tanzania',
         'Eritrea', 'Nigeria', 'South Africa')


country_conversion  <- tibble('country'=countries, 'country_name'=names) %>% arrange(country_name)


country_choice <- dlg_list(choices = country_conversion$country_name,
                   multiple = TRUE,
                   title = "Select Countries")$res

selected_countries <- country_conversion %>% filter(country_name %in% country_choice)


country_url <- paste(selected_countries$country, collapse = "&country=")


# Available indicators - Missing all  ANC indicators (No estimates for many countries)
indicator = c('population', 'prevalence', 'plhiv', 'art_coverage',
             'art_current_residents', 'art_current', 'untreated_plhiv_num',
             'aware_plhiv_prop', 'unaware_plhiv_num', 'aware_plhiv_num',
             'plhiv_attend','untreated_plhiv_attend', 'aware_plhiv_attend',
             'unaware_plhiv_attend', 'incidence', 'infections', 'anc_prevalence',
             'anc_art_coverage','anc_clients', 'anc_plhiv', 'anc_already_art',
             'anc_art"new', 'anc_known_pos', 'anc_tested_pos', 'anc_tested_neg')

indicator_names <- c('Population', 'HIV Prevalence', 'PLHIV',
                     'ART Coverage', 'ART Number (Residents)',
                     'ART Number (Attending)', 'PLHIV not on ART',
                     'Proportion PLHIV Aware', 'Number Unaware PLHIV',
                     'Number PLHIV Aware', 'PLHIV (ART catchment)', 'Untreated PLHIV (ART catchment)',
                     'Number aware PLHIV (ART catchment)', 'Number unaware PLHIV (ART catchment)', 'HIV Incidence',
                     'New Infections', 'ANC HIV Prevalence', 'ANC Prior ART Coverage', 
                     'ANC Clients', 'HIV Positive ANC Attendees', 'ANC Attendees already on ART',
                     'ART Initiations at ANC', 'ANC Known Positive', 'ANC Tested Positive', 'ANC Tested Negative'
)
indicator_conversion  <- tibble('indicator'=indicator, 'indicator_name'=indicator_names) %>% arrange(indicator_name)

indicator_choice <- dlg_list(choices = indicator_conversion$indicator_name,
                           multiple = TRUE,
                           title = "Select Countries")$res

indicator_choice <- (indicator_conversion %>% filter(indicator_name %in% indicator_choice))$indicator

# Age Groups
ageGroup = c('Y015_049', 'Y015_064', 'Y015_999', 'Y050_999', 'Y000_999',
            'Y000_064', 'Y000_014', 'Y015_024', 'Y025_034', 'Y035_049',
            'Y050_064', 'Y065_999', 'Y010_019', 'Y025_049', 'Y000_004',
            'Y005_009', 'Y010_014', 'Y015_019', 'Y020_024', 'Y025_029',
            'Y030_034', 'Y035_039', 'Y040_044', 'Y045_049', 'Y050_054',
            'Y055_059', 'Y060_064', 'Y065_069', 'Y070_074', 'Y075_079',
            'Y080_999', 'Y000_000', 'Y001_004')

age_name = c('15-49', '15-64', '15+', '50+', 'All ages',
             '0-64', '0-14', '15-24', '25-34', '35-49',
             '50-65', '65+', '10-19', '25-49', '0-4',
             '5-9', '10-14', '15-19', '20-24', '25-29',
             '30-34', '35-39', '40-44', '45-49', '50-54',
             '55-59', '60-64', '65-69', '70-74', '75-79',
             '80+', '<1', '1-4')

age_conversion  <- tibble('ageGroup'=ageGroup, 'age_name'=age_name)

age_choice <- dlg_list(choices = age_conversion$age_name,
                             multiple = TRUE,
                             title = "Select Countries")$res

age_choice <- (age_conversion %>% filter(age_name %in% age_choice))$ageGroup

# Periods
period = c('2021-3', '2022-4', '2023-3', '2023-4', '2024-3','2024-4', '2025-3', '2025-4', '2026-3', '2026-4')

period_names = c('September 2021', 'December 2022', 
                 'September 2023', 'December 2023', 
                 'September 2024','December 2024', 
                 'September 2025', 'December 2025', 
                 'September 2026', 'December 2026')

period_conversion <- tibble(period = period, names = period_names)

period_choice <- dlg_list(choices = period_conversion$names,
                                           multiple = TRUE,
                                           title = "Select Time Period")$res
period_choice <- (period_conversion %>% filter(names %in% period_choice))$period


# Sex
sex = c('both', 'male', 'female')

sex_choice <- dlg_list(choices = sex,
                                              multiple = TRUE,
                                              title = "Select Sex")$res

# Area Level - 3 is the preferred area level
areaLevel = c('1', '2', '3', '4')

area_choice <- dlg_list(choices = areaLevel,
                                              multiple = TRUE,
                                              title = "Select area granularity")$res
are_choice <- c(0, area_choice)

url_temp1 <- list()
url_temp2 <- list()
url_temp3 <- list()
url_temp4 <- list()
url_temp5 <- list()

for (x in area_choice) {
  for (i in indicator_choice) {
    for (j in age_choice) {
      for (m in period_choice) {
        for (n in sex_choice) {
          temp_1 <- tibble(
            'indicator' = i,
            'age' = j,
            'period' = m,
            'sex' = n,
            'areaLevel' = x)
          url_temp1[[n]] <- temp_1
        }
        temp_2 <- bind_rows(url_temp1)
        url_temp2[[m]] <- temp_2
      }
      temp_3 <- bind_rows(url_temp2)
      url_temp3[[j]] <- temp_3
    }
    temp_4 <- bind_rows(url_temp3)
    url_temp4[[i]] <- temp_4
  }
  temp_5 <- bind_rows(url_temp4)
  url_temp5[[x]] <- temp_5
}
url_ends <- list()
url_ends <- bind_rows(url_temp5)


url <- url_ends %>% mutate(url = str_c(base_url,
                          "country=", country_url, 
                          "&indicator=", indicator,
                          "&ageGroup=", age,
                          "&period=", period,
                          "&sex=", sex,
                          "&areaLevel=", areaLevel))
 
data <- list()
for (i in 1:nrow(url)) {
  download.file(url$url[i],
                "data/temp/data.csv")
  df <- read_csv("data/temp/data.csv") 
  
  if (nrow(df)>=1) {
    data[[i]] <- df %>%   
    mutate(indicator = url$indicator[i],
           age = url$age[i],
           period = url$period[i], 
           sex = url$sex[i])
  }
}

df <- bind_rows(data)

x <- which(df$level == 0)
z <- which(df$level != 0)

df$country <- df$area
df$country[df$level != 0] <- df$area[x[sapply(z, function(i) findInterval(i,x))]]

a <- df %>% 
  left_join(indicator_conversion, by = c("indicator")) %>% 
  left_join(age_conversion, by = c("age" = "ageGroup")) %>%
  left_join(period_conversion, by = c("period")) %>% 
  relocate(indicator_name, .after = "indicator") %>% 
  relocate(age_name, .after = "age") %>% 
  relocate(names, .after = "period") %>% 
  relocate(country, .after = "level") %>% 
  rename("period_name" = "names")
  
 
write_csv(df, str_c("data/output/naomi_output",  today(), ".csv"))