require("ggplot2")

# Read input data
data.file <- commandArgs(trailingOnly = TRUE)[1]
data <- read.csv(file = data.file, header = TRUE)

# Categorical variables as character
data$Exp.. <- as.character(data$Exp..)
data$Nodes <- as.character(data$Nodes)
data$Population <- as.character(data$Population)

# Sum up iteration times as they are stored as times between new best length findings
data$Elapsed.Time <- ave(data$Elapsed.Time,
                         data$Exp.., data$Nodes, data$Population,
                         FUN=cumsum)


#print(head(data[, c(1,2,3,5,7,8)], n=30))
summary(data)

# Summarize data of the repetitions of the experiments
mean.Best.Length <- aggregate(data$Best.Length,
                              list(Nodes = data$Nodes,
                                   Population = data$Population,
                                   Iteration = data$Iteration),
                              mean)

mean.Elapsed.Time <- aggregate(data$Elapsed.Time,
                               list(Nodes = data$Nodes,
                                    Population = data$Population,
                                    Iteration = data$Iteration),
                               mean)

summarized.data <- mean.Best.Length[, c(1, 2, 3)]

summary(summarized.data)

summarized.data$mean.Best.Length <- mean.Best.Length$x
summarized.data$mean.Elapsed.Time <- mean.Elapsed.Time$x

summary(summarized.data)


# Charts

# Best length x Iteration

regression.chart.Best.Length <- function(data)
    ggplot(data, aes(x=Iteration, y=mean.Best.Length, color=Population, fill=Population, shape=Nodes)) +
        geom_point() +
        #geom_line() +
        geom_smooth()

#regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 10 & summarized.data$Iteration < 50, ])
#regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 10 & summarized.data$Iteration < 50, ])

regression.chart.Best.Length(summarized.data)
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 10, ])
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 10 & summarized.data$Population != 3, ])
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 30, ])
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 30 & summarized.data$Population != 2, ])
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 60, ])

png(file="regression-chart-best-length.png")
regression.chart.Best.Length(summarized.data)
dev.off()

png(file="regression-chart-best-length-60.png")
regression.chart.Best.Length(summarized.data[summarized.data$Nodes == 60, ])
dev.off()

# Best length x Elapsed.Time

regression.chart.Elapsed.Time <- function(data)
    ggplot(data, aes(x=mean.Elapsed.Time, y=mean.Best.Length, color=Population, fill=Population, shape=Nodes)) +
        geom_point() +
        #geom_line() +
        geom_smooth()

regression.chart.Elapsed.Time(summarized.data)
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 10, ])
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 10 & summarized.data$Population != 3, ])
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 30, ])
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 30 & summarized.data$Population != 2, ])
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 60, ])

png(file="regression-chart-elapsed-time.png")
regression.chart.Elapsed.Time(summarized.data)
dev.off()

png(file="regression-chart-elapsed-time-60.png")
regression.chart.Elapsed.Time(summarized.data[summarized.data$Nodes == 60, ])
dev.off()

# Elapsed.Time x Nodes X Population

chart.Elapsed.Time.Iterations <- function(data)
    ggplot(data, aes(x=(as.integer(Nodes) + as.integer(Population)), y=mean.Elapsed.Time, color=Iteration, fill=Iteration)) +
        geom_point()# +
        #geom_line()# +
        #geom_smooth()

chart.Elapsed.Time.Iterations(summarized.data)
chart.Elapsed.Time.Iterations(summarized.data[summarized.data$Nodes == "10",])
chart.Elapsed.Time.Iterations(summarized.data[summarized.data$Nodes == "30",])
chart.Elapsed.Time.Iterations(summarized.data[summarized.data$Nodes == "60",])

png(file="time-iterations-chart.png")
chart.Elapsed.Time.Iterations(summarized.data)
dev.off()

png(file="time-iterations-chart-60.png")
chart.Elapsed.Time.Iterations(summarized.data[summarized.data$Nodes == "60",])
dev.off()
