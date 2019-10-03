<?php
  require_once __DIR__ . '/vendor/autoload.php';
  use PhpAmqpLib\Connection\AMQPStreamConnection;
  use PhpAmqpLib\Message\AMQPMessage;

  echo 'If it gets to this point, then it works.'
?>
