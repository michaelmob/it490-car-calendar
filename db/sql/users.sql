DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `email` varchar(256) NOT NULL,
  `username` varchar(256) NOT NULL,
  `password` varchar(256) NOT NULL,
  `salt` varchar(256) NOT NULL,
  `token` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `unique_email` UNIQUE (`email`),
  CONSTRAINT `unique_username` UNIQUE (`username`),
  CONSTRAINT `unique_token` UNIQUE (`token`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
