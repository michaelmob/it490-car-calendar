<?php
require_once __DIR__ . '/vendor/autoload.php';
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;



class AuthRpcClient {
    private $connection;
    private $channel;
    private $callback_queue;
    private $response;
    private $corr_id;

    public function __construct($host, $port, $vhost, $username, $password) {
        // Create rabbitmq connection
        $this->connection = new AMQPStreamConnection(
            $host, $port, $username, $password
        );

        // Set up callback queue
        $this->channel = $this->connection->channel();
        list($this->callback_queue, ,) = $this->channel->queue_declare(
            '', false, false, true, false
        );

        // Consume responses before sending
        $this->channel->basic_consume(
            $this->callback_queue, '',
            false, true, false, false,
            array($this, 'onResponse')
        );
    }


    public function onResponse($response) {
        if ($response->get('correlation_id') == $this->corr_id)
            $this->response = $response->body;
    }


    public function call($username, $email, $password) {
        $this->response = null;
        $this->corr_id = uniqid();

        // Send the request
        $msg = new AMQPMessage((string) $n,
            array(
                'correlation_id' => $this->corr_id,
                'reply_to' => $this->callback_queue
            )
        );

        $this->channel->basic_publish($msg, '', 'rpc_queue');

        // Wait for response...
        while (!$this->response)
            $this->channel->wait();

        return $this->response;
    }

}
?>
