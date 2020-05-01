library(googlesheets4)
library(reshape2)
library(dplyr)
library(stringr)
library(data.table)
library(lubridate)

sheets_auth()

ssID <- "1gR03lPiOBDiQOd3XFhSkYWJWi1vG8Wf_J-nmtSRaXbk"
worksheets <- c("daily new infections", "interventions", "melted viz data")
dailyNewInfections <- read_sheet(ss = ssID,sheet = worksheets[1])
interventions <- read_sheet(ss = ssID, sheet = worksheets[2])

epidemicStart <- ymd("2020-01-24")

idVars <- c("Date")
keyVars <- c(idVars, "region")
regions <- c("NSW", "WA", "VIC", "SA", "ACT", "NT", "QLD", "TAS", "AUS")
newInfections <- str_c(regions, c(" new"))

totalCases <- reshape2::melt(
  dailyNewInfections,
  measure.vars = regions,
  id.vars = idVars,
  variable.name = "region",
  value.name = "total confirmed cases"
) %>% data.table(key = keyVars)

newDailyCases <- reshape2::melt(
  dailyNewInfections,
  measure.vars = newInfections,
  id.vars = idVars,
  variable.name = "region",
  value.name = "new cases"
) %>% data.table(., key = keyVars)

# strip "new" from levels of "region"
levels(newDailyCases$region) <- regions

meltedInterventions <- reshape2::melt(
  interventions,
  measure.vars = regions,
  id.vars = idVars,
  variable.name = "region",
  value.name = "interventions"
) %>% data.table(., key = keyVars)

totalCases[newDailyCases[meltedInterventions]]

totalNewAndInterventions <-
  left_join(totalCases, newDailyCases, by = keyVars) %>%
  left_join(y = meltedInterventions, by = keyVars) %>%
  data.table

totalNewAndInterventions %>%
  write.csv(file="./TMR stuff/TMR/covid-19/code/meltedData.csv",
            row.names = FALSE)



# write melted data to gsheet
ss <- googledrive::drive_get(id=ssID)
sheet_write(data = totalNewAndInterventions, ss = ss, sheet = worksheets[3])

