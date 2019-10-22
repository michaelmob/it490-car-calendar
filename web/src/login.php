<?php
	require_once __DIR__ . 'vendor/autoload.php';
	use PhpAmqpLib\Connection\AMQPStreamConnection;
	use PhpAmqpLib\Message\AMQPMessage;

	$user_name = $_POST["username"];
	$pass_word = $_POST["password"];
	//Establishes RabbitMQ Connection
	$host = "";
	$port = "";
	$username = "";
	$password = "";
	$vhost = "";
	$exchange = "";
	$queue = "";
	$connection = new AMQPStreamConnection($host, $port, $username, $password);
	//Sending Messages
	$sending_channel = $connection->channel();
	$sending_channel->queue_declare('auth', false, false, false, false);
	$msg = new AMQPMessage('$user_name\n$pass_word');
	$sending_channel->basic_publish($msg, '', 'auth');
	echo " [x] $user_name\n$pass_word\n";
	$sending_channel->close();
	//$connection->close();
	//Receiving Messages
	$receiving_channel = $connection->channel();
	$receiving_channel->queue_declare('auth', false, false, false, false);
	echo " [x] Waiting for return messages...";
	$callback = function ($msg) {
		echo ' [x] ', $msg->body, "\n";
	};
	$receiving_channel->basic_consume('auth', '', false, true, false, false, $callback);
	while ($receiving_channel->is_consuming()){
		$channel->wait();
	}
	//Closing The Connection
	$connection->close();
?>
