library(ggplot2)
library(gridExtra)
library(argparse)

parser <- ArgumentParser(description='Process motor data to create graphs')
parser$add_argument('input', metavar='input path', type='character',
                    nargs=1, help='A csv file created by Rhoban LogService')
parser$add_argument('--output', metavar='output path', type='character',
                    default='tmp.png',
                    help='The file to which the graph is saved')
parser$add_argument('--variable', metavar='variable displayed', type='character',
                    default='temperature',
                    choices= c('temperature','warnings','errors','missings'),
                    help='The name of the variable to display')

args <- parser$parse_args()

data <- read.csv(args$input)

# Ordering the levels of motor_name makes sure that order in plots is meaningful
# - One row for each leg, one row for both shoulder + one row for head
# - Inside each part, elements are order from the closest to the trunk until the end
data$motor_name <- ordered(data$motor_name,
                           levels = c(
                               "left_hip_yaw", "left_hip_roll", "left_hip_pitch",
                               "left_knee", "left_ankle_pitch", "left_ankle_roll",
                               "right_hip_yaw", "right_hip_roll", "right_hip_pitch",
                               "right_knee", "right_ankle_pitch", "right_ankle_roll",
                               "left_shoulder_pitch", "left_shoulder_roll", "left_elbow",
                               "right_shoulder_pitch", "right_shoulder_roll", "right_elbow",
                               "head_yaw", "head_pitch"))

g <- ggplot(data, aes_string(x='time',y=args$variable,group='motor_name'))
g <- g + geom_line()
g <- g + facet_wrap(.~motor_name,ncol=6)
ggsave(args$output,width=10,height=6)


# Unused Currently: attributing body names
# Adding data part: currently unused
## data$body_level <- "head"
## data$body_level[which(grepl("elbow",data$motor_name))] <- "arm"
## data$body_level[which(grepl("shoulder",data$motor_name))] <- "arm"
## data$body_level[which(grepl("hip",data$motor_name))] <- "leg"
## data$body_level[which(grepl("knee",data$motor_name))] <- "leg"
## data$body_level[which(grepl("ankle",data$motor_name))] <- "leg"
## data$side <- "central"
## data$side[which(grepl("left",data$motor_name))] <- "left"
## data$side[which(grepl("right",data$motor_name))] <- "right"
## data$body_part <- paste(data$body_level, data$side,sep = '_')
