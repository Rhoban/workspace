library(ggplot2)
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

g <- ggplot(data, aes_string(x='time',y=args$variable,group='motor_name'))
g <- g + geom_line()
g <- g + facet_wrap(~motor_name)
ggsave(args$output)
