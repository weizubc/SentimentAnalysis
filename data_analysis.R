#clear window
rm(list=ls())
setwd("/Volumes/mac/users/w/sentiment")
weather <- read.csv('weather.csv')
sent_sf <- read.table('result_sf.txt')
colnames(sent_sf) <- c("year","month","day","weekday","hour","tweets","sentiment")
sent_sf$weekday <- sent_sf$weekday + 1
#define sentiment as the fraction of positive tweets
sent_sf$sentiment <- 1- sent_sf$sentiment

#clean weather data
#split column time into hour, minute and am/pm
out <- strsplit(as.character(weather$time),' ')
weather$hour <- do.call(rbind, out)[,1]
weather$ampm <- do.call(rbind, out)[,2]
out <- strsplit(as.character(weather$hour),':')
weather$hour <- do.call(rbind, out)[,1]
weather$minute <- do.call(rbind, out)[,2]

#convert hour to 24 format
weather$hour <- with (weather, ifelse(hour == 12, 0, hour))
weather$hour <- with (weather, ifelse(ampm == "PM", as.integer(hour) + 12, hour))

#remove % in column humidity
out <- strsplit(as.character(weather$humidity),'%')
weather$humidity_num <- do.call(rbind, out)[,1]
weather$humidity <- as.integer(weather$humidity_num)

#convert column windspeed to numeric
out <- strsplit(as.character(weather$windspeed),'Calm')
weather$windspeed_num <- do.call(rbind, out)[,1]
weather$windspeed <- as.numeric(weather$windspeed_num)
weather[is.na(weather)] <- 0

#regroup weather condition categorial variable
weather$rain <- with (weather, ifelse(conditions == "Heavy Rain" | conditions == "Light Rain" | conditions == "Rain", 1, 0))
weather$sunny <- with (weather, ifelse(conditions == "Clear", 1, 0))
weather$conditions <- with(weather, ifelse(rain == 1, "Rain", "Cloudy"))
weather$conditions <- with(weather, ifelse(sunny == 1, "Sunny", conditions))

#remove duplicates  within the same hour and keep the last copy at the latest observation time
dups <- weather[c("month","day","hour")]
weather <- weather[!duplicated(dups,fromLast=TRUE),]
weather_sf <- weather[c("month","day","hour","temp","conditions","humidity","windspeed")]

#merge sentiment and weather dataframes and use left join 
combine <- merge(x=sent_sf, y=weather_sf, by=c("month","day","hour"), all.x=TRUE)



#do analysis
data <- subset(combine, tweets>=100 & !is.na(temp))

data$daytime <- factor(with (data, ifelse(hour >=8 & hour<= 18, "Day", "Night")))
data$weekday <- factor(data$weekday)
data$tempsq <- (data$temp)**2

summary(data)

#graph
library(ggplot2)
library(gridExtra)

p1 <- qplot(x=sentiment,data=data)
groupmean <- aggregate(sentiment ~ daytime + weekday,data,mean)
p2 <- qplot(weekday,sentiment, data=groupmean,geom="point", xlab="day of week", ylab="sentiment mean", colour=daytime)
#groupmean <- aggregate(sentiment ~ hour + fweekday,data,mean)
#qplot(hour,sentiment, data=groupmean,geom=c("line","point"), xlab="hour", ylab="sentiment mean", colour=fweekday)


groupmean <- aggregate(sentiment ~ daytime + conditions,data,mean)
p3 <- qplot(conditions,sentiment, data=groupmean,geom="point", xlab="weather", ylab="sentiment mean", colour=daytime)


p4 <- qplot(x=temp,y=sentiment,data=data, geom=c("smooth","point"), xlab="temperature")

grid.arrange(p1,p2,p3,p4,nrow=2,ncol=2)

#regression
#linear model
m1 <- lm(sentiment ~ daytime + weekday + conditions + temp + tempsq, data=data )
summary(m1)

#fractional logit model
m2 <- glm(cbind(tweets*sentiment, tweets) ~ daytime + weekday + conditions + temp + tempsq,
          family=binomial(logit), data=data)
summary(m2)



