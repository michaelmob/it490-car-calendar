<?php
require_once __DIR__ . '/vendor/autoload.php';

// Ensure request is a POST request
if (empty($_POST)) {
    header("HTTP/1.1 401 Unauthorized");
    exit(0);
}

$result = ['message' => '', 'success' => false];

/**
 * Helper function
 * Check for POST value or exit.
 */
function checkField($field) {
    if (isset($_POST[$field]))
        return;

    $result['message'] = "Missing '$field' field.";
    echo(json_encode($result));
    exit(0);
}

checkField('username');  // Ensure username field is set
checkField('password');  // Ensure password field is set

if ($success) {
    $result['success'] = true;
    $result['message'] = 'Auth successful.';
}

echo(json_encode($result));
?>
