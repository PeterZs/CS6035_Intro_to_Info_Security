<?php
// start the session
session_start();
// initialize authentication functions
require_once('auth.php');
// initialize database - sqlite is pretty similar to mysql
require_once('sqlite.php');
// Allow users to use the back button without reposting data
header ("Cache-Control: private");

// initialize the objects defined in the above php files
$db   = new Database('/var/payroll/db/payroll.db');
$auth = new Auth($db);

// notification system
function notify($string, $success = 0) {
	$type = 'notify';
	if ($success == -1) $type = 'error';
	if ($success == 1) $type = 'success';
	$_SESSION['notification'] = array('type' => $type, 'message' => $string);
}

// on any page, if the logout parameter is set, log the user out
if (isset($_GET['logout'])) {
	$auth->logout();
	header('location: /');
}
?>
