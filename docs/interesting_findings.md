Note: this file is not polished, for now it is just used to document all noteworthy findings

-At noise SD around equal to signal range, wiener filter is around an order of magnitude more effective than the inverse filter and BGD
-At noise SD > 10% of range, Wiener filter achieves best accuracy at zero pad lengths less than or equal to the signal length. Error from setting the zero pad length to the signal length averages to less than 10% greater than the minimum error in that interval. The exact error depends on the signal length itself.
-inverse filter and bgd have very similar errors