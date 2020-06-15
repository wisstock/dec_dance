require(ggplot2)
# require(plotly)
# require(magrittr)

# wd_path <- strsplit(rstudioapi::getSourceEditorContext()$path, '/')
setwd(paste(paste(strsplit(rstudioapi::getSourceEditorContext()$path, '/')[[1]][1:4], collapse='/'),'/model_snr_fill', sep=''))

df <- read.csv('snr_res.csv')
df$iter[df$iter==0]=6


df_sd <- subset(df, init_sd > 2 & init_snr == 50)

ggplot(df_sd, aes(x=iter, y=sum, colour=as.factor(init_sd))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  geom_hline(yintercept=2501400.0, linetype="dashed", color = "red") +  # raw sum
  annotate("text", label = "Native summ", x = 600, y = 2506400.0,       # 4392000.0 for circ
           colour="red",  family = 'oswald', size = 6) +
  geom_hline(yintercept=2424615.0, linetype="dashed", color = "red") +  # conv sum
  annotate("text", label = "Convolve summ", x = 600, y = 2429615.0,     # 4192392.5 for circ
         colour="red", family = 'oswald', size = 6) +
  coord_trans(x="log2") +
  scale_x_continuous(breaks = c(6, 8, 16, 32, 64, 128, 256, 512, 1024),
                     label = c(0, 8, 16, 32, 64, 128, 256, 512, 1024)) +
  scale_y_continuous(labels = function(x) format(x, scientific = TRUE)) +
  labs(x ='Iteration', y = 'Sum. intensity') +
  guides(color=guide_legend(title='I mean/SD (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')




selected_sd <- 5

df_mod <- subset(df, init_sd == selected_sd & init_snr > 1,
                 select = c(PSNR, init_snr, iter))

ggplot(df_mod, aes(x=iter, y=PSNR, colour=as.factor(init_snr))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  coord_trans(x="log2") +
  scale_x_continuous(breaks = c(6, 8, 16, 32, 64, 128, 256, 512, 1024),
                     label = c(0, 8, 16, 32, 64, 128, 256, 512, 1024)) +
  scale_y_continuous(limits = c(8, 20), breaks = seq(8, 20, 1)) +
  labs(title = sprintf('Noise SD = %sdB', selected_sd),
       x ='Iteration', y = 'PSNR (dB)') +
  guides(color=guide_legend(title='Initial SNR (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')


# df_surf <- subset(df, iter == 128, select = c(PSNR, init_SNR, init_sd))
# mat_surf <- data.matrix(df_surf)
# a <- plot_ly(z = ~mat_surf)
# add_surface(a)

# ggplot(df_surf, aes(x=init_SNR, y=init_sd, z=PSNR)) +
#   coord_trans(x='log10') +
#   geom_contour(bins=50)

selected_iter = 64
df_sd <- subset(df, iter == selected_iter & init_snr > 1,
                select = c(PSNR, init_snr, init_sd))

ggplot(df_sd, aes(x=init_sd, y=PSNR, colour=as.factor(init_snr))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  scale_y_continuous(limits = c(7, 20), breaks = seq(7, 20, 1)) +
  scale_x_reverse(breaks = c(0, 2, 5, 10, 15, 20, 25)) +
  labs(title = sprintf('Iteration %s', selected_iter),
       x ='I mean/SD (dB)', y = 'PSNR (dB)') +
  guides(color=guide_legend(title='Initial SNR (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')
