<?php
	require_once __DIR__ . '/vendor/autoload.php';
	use PhpAmqpLib\Connection\AMQPStreamConnection;
	use PhpAmqpLib\Message\AMQPMessage;
	$first_name = $_GET["first"];
	$last_name = $_GET["last"];
	$email = $_GET["email"];
	$user_name = $_GET["uname"];
	$password = $_GET["password"];
	echo "$first_name $last_name $email $user_name $password";
	//$connection = new AMQPStreamConnection('192.168.1.111', 5672, 'admin', 'adminpass');
	//$channel = $connection->channel();
	//$channel->queue_declare('log-queue', false, false, false, false);
	//$msg = new AMQPMessage('Hello World!');
	//$channel->basic_publish($msg, '', 'hello');
	//echo " [x] Sent 'Hello World!'\n";
	//$channel->close();
	//$connection->close();
?>

