require(ggplot2)
# require(plotly)
# require(magrittr)

# wd_path <- strsplit(rstudioapi::getSourceEditorContext()$path, '/')
setwd(paste(paste(strsplit(rstudioapi::getSourceEditorContext()$path, '/')[[1]][1:4], collapse='/'),'/model_snr', sep=''))

df <- read.csv('snr_res.csv')
df$iter[df$iter==0]=6

selected_sd = 25
df_mod <- subset(df, init_sd == selected_sd & init_SNR > 1,
                 select = c(PSNR, init_SNR, iter))

ggplot(df_mod, aes(x=iter, y=PSNR, colour=as.factor(init_SNR))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  coord_trans(x="log2") +
  scale_x_continuous(breaks = c(6, 8, 16, 32, 64, 128, 256, 512, 1024),
                     label = c(0, 8, 16, 32, 64, 128, 256, 512, 1024)) +
  scale_y_continuous(limits = c(12, 20), breaks = seq(10, 20, 1)) +
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

selected_iter = 1024
df_sd <- subset(df, iter == selected_iter & init_SNR > 1,
                select = c(PSNR, init_SNR, init_sd))

ggplot(df_sd, aes(x=init_sd, y=PSNR, colour=as.factor(init_SNR))) +
  geom_line(size=1) +
  geom_point(size=1.5) +
  scale_y_continuous(limits = c(12, 20), breaks = seq(10, 20, 1)) +
  scale_x_reverse(breaks = c(0, 2, 5, 10, 15, 20, 25)) +
  labs(title = sprintf('Iteration %s', selected_iter),
       x ='I mean/SD (dB)', y = 'PSNR (dB)') +
  guides(color=guide_legend(title='Initial SNR (dB)', reverse=T)) +
  theme_minimal(base_size = 20, base_family = 'oswald')
