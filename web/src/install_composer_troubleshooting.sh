sudo apt-get install composer		#installs composer
sudo chown -R $USER .composer		#give current user ownership of the hidden .composer direcotry
sudo chmod 777 .composer		#give all permissions for the hidden composer directory exists either in current working directory or the home directory ~/.composer
sudo apt install php7.2-bcmatch		#installs php7.2-bcmatch dependency
sudo chmod -R 777 < pwd			#give all permissions for the current working directory
composer require php-amqplib/php-amqplib #implements the php-amqplib into composer
