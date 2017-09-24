#### this creates two pie-charts in one picture to show the ratio of major translation errors in EN>RU and RU>EN
#### the input data format: tsv error_type(standars RusLTC categories)  nums    lang(ENRU/RUEN)
#### mkunilovskaya, September 22, 2017  
library(ggplot2)
df = read.csv('/home/masha/both_distribution_allann_tidy.csv')

#subset the dataframe
ru_cont_ref = sum(df$nums[1:7])
ru_cont_coh = sum(df$nums[8:10])
ru_cont_pr = sum(df$nums[11:13])
ru_lang_lex = sum(df$nums[14:17])
ru_lang_mor = sum(df$nums[18:19])
ru_lang_synt = sum(df$nums[20:25])
ru_lang_hyg = sum(df$nums[26:29])
ru_total = sum(df$nums[1:29])
ru_total

ru_errors_tidy = c(ru_cont_ref,ru_cont_coh,ru_cont_pr,ru_lang_lex,ru_lang_mor,ru_lang_synt,ru_lang_hyg)

en_cont_ref = sum(df$nums[33:39])
en_cont_coh = sum(df$nums[40:42])
en_cont_pr = sum(df$nums[43:45])
en_lang_lex = sum(df$nums[46:49])
en_lang_mor = sum(df$nums[50:51])
en_lang_synt = sum(df$nums[52:57])
en_lang_hyg = sum(df$nums[58:61])
en_total = sum(df$nums[33:61])
en_total

en_errors_tidy = c(en_cont_ref,en_cont_coh,en_cont_pr,en_lang_lex,en_lang_mor,en_lang_synt,en_lang_hyg)

#recreate dataframe with aggregated counts for major error_types
df_major <- data.frame(error_types = c('reference','cohesion','pragmatics','lexis','morphology','syntax','hygiene', 'reference','cohesion','pragmatics','lexis','morphology','syntax','hygiene'),
                        nums = c(ru_errors_tidy, en_errors_tidy),
                        lang = c(rep('ENRU', 7), rep('RUEN', 7)))
#looks ok
df_major

#this produces a stacked bar-chart
p = ggplot(data=df_major, aes(x = factor(1), y = c(nums), fill = factor(df_major$error_types, levels = c('reference','cohesion','pragmatics','lexis','morphology','syntax','hygiene'))))
p
p=p + geom_bar(stat = "identity", width = 1)
p
p=p+facet_grid(facets=. ~ lang) # Divide by levels of "lang", in the horizontal direction
p

#turn it into pie
p = p + coord_polar(theta="y")
p

#to make charts comparable render absolute counts as percentages in a new column Pct
df_major$Pct[1:7] <- df_major$nums[1:7] / ru_total*100
df_major$Pct[8:14] <- df_major$nums[8:14] / en_total*100
df_major

#округляем до десятых, добавляем знак процента
percentlabels <- round(df_major$Pct, 1)
pielabels<- paste(percentlabels, "%", sep="")

#еще раз рисуем график, меняем название легенды
p = ggplot(data=df_major, aes(x = factor(1), y = c(Pct), fill = factor(df_major$error_types, levels = c('reference','cohesion','pragmatics','lexis','morphology','syntax','hygiene'))))
p=p + geom_bar(stat = "identity", width = 1)
p
# модифицируем подписи панелей (=facets) на labels = c("EN>RU (648 texts, 11160 tags)", "RU>EN (312 texts, 3956 tags)") 
# from http://www.cookbook-r.com/Graphs/Facets_(ggplot2)/ There are a few different ways of modifying facet labels. 
# The simplest way is to provide a named vector that maps original names to new names. To map the levels of sex from Female==>Women, and Male==>Men
# labels <- c(Female = "Women", Male = "Men")
# sp + facet_grid(. ~ sex, labeller=labeller(sex = labels))
labels <- c(ENRU = "EN>RU (648 texts, 11160 tags)", RUEN = "RU>EN (312 texts, 3956 tags)")
p=p+facet_grid(facets=. ~ lang, labeller=labeller(lang = labels)) # Divide by levels of "lang", in the horizontal direction
p



p=p+ labs(fill='Major error types')
# добавляем название всей картинки "Distibution of error types in EN<>RU translations (in %)"
p=p+ggtitle("Distibution of error types in EN<>RU learner translations (in %)")
p


#turn it into pie and delete prop elements
p = p + coord_polar(theta="y")
p = p + theme(axis.text.x=element_blank(),
              axis.text.y=element_blank(),axis.ticks=element_blank(),
              axis.title.x=element_blank(),
              axis.title.y=element_blank(),panel.grid=element_blank(), panel.border=element_blank(),
              panel.grid.major = element_blank(),
              panel.grid.minor = element_blank(),
              panel.spacing = unit(0, "lines"))
p
# добавляем подписи значений для каждой категории
p=p + geom_text(aes(label = pielabels), size = 4, position = position_stack(vjust = 0.5))
p



