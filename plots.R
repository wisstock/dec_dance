require(ggplot2)
# require(plotly)

setwd(paste(paste(strsplit(rstudioapi::getSourceEditorContext()$path, '/')[[1]][1:4], collapse='/'),'/model_snr_circ', sep=''))

df <- read.csv('snr_res.csv')
df$iter[df$iter==0]=6


#### INTENSITY SUM PLOT #####
df_sum <- subset(df, init_snr == 50)

ggplot(df_sum, aes(x=iter, y=sum, colour=as.factor(init_sd))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  geom_hline(yintercept=4392000.0, linetype="dashed", color = "red") +  # raw sum
  annotate("text", label = "Native summ", x = 600, y = 4402000.0,       # 4392000.0 for circ, 2501400.0 for fill
           colour="red",  family = 'oswald', size = 6) +
  geom_hline(yintercept=4192392.5, linetype="dashed", color = "red") +  # conv sum
  annotate("text", label = "Convolve summ", x = 600, y = 4202392.5,     # 4192392.5 for circ, 2424615.0 for fill
         colour="red", family = 'oswald', size = 6) +
  coord_trans(x="log2") +
  scale_x_continuous(breaks = c(6, 8, 16, 32, 64, 128, 256, 512, 1024),
                     label = c(0, 8, 16, 32, 64, 128, 256, 512, 1024)) +
  scale_y_continuous(labels = function(x) format(x, scientific = TRUE)) +
  labs(x ='Iteration', y = 'Sum. intensity') +
  guides(color=guide_legend(title='I mean/SD (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')



##### SELECTED SD PLOT #####
selected_sd <- 25

df_sd <- subset(df, init_sd == selected_sd & init_snr > 1,
                 select = c(PSNR, init_snr, iter))

ggplot(df_sd, aes(x=iter, y=PSNR, colour=as.factor(init_snr))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  coord_trans(x="log2") +
  scale_x_continuous(breaks = c(6, 8, 16, 32, 64, 128, 256, 512, 1024),
                     label = c(0, 8, 16, 32, 64, 128, 256, 512, 1024)) +
  scale_y_continuous(limits = c(8, 20.3), breaks = seq(8, 20, 1)) +
  labs(title = sprintf('Noise SD = %sdB', selected_sd),
       x ='Iteration', y = 'PSNR (dB)') +
  guides(color=guide_legend(title='Initial SNR (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')



##### SELECTED ITER PLOT #####
selected_iter = 1024

df_iter <- subset(df, iter == selected_iter & init_snr > 1,
                select = c(PSNR, init_snr, init_sd))

ggplot(df_iter, aes(x=init_sd, y=PSNR, colour=as.factor(init_snr))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  scale_y_continuous(limits = c(7, 20.3), breaks = seq(7, 20, 1)) +
  scale_x_reverse(breaks = c(0, 2, 5, 10, 15, 20, 25)) +
  labs(title = sprintf('Iteration %s', selected_iter),
       x ='I mean/SD (dB)', y = 'PSNR (dB)') +
  guides(color=guide_legend(title='Initial SNR (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')
