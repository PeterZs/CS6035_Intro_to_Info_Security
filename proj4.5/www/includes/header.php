<!DOCTYPE html>
<html>
 <head>
  <title>Georgia Tech Payroll System</title>
  <link href="/assets/bootstrap/css/bootstrap.css" rel="stylesheet" type="text/css">
  <link href="/assets/screen.css" rel="stylesheet" type="text/css">
  <link href="/assets/bootstrap/css/bootstrap-responsive.css" rel="stylesheet" type="text/css">
 </head>
 <body>
  <div class="container header">
   <img src="/assets/banner.png">
   <h1>Georgia Tech</h1>
   <h2>Accounting and Payroll System</h2>
<?php if ($auth->user_id()): ?>
   <p>You are logged in as <?php echo $auth->name() ?> (<?php echo $auth->eid() ?>) - <a href="?logout">Log out</a></p>
<?php endif; ?>
  </div>
  <div class="container main">
<?php if (@$_SESSION['notification']): ?>
  <div class="alert alert-<?php echo $_SESSION['notification']['type'] ?>">
   <button type="button" class="close" data-dismiss="alert" data-identifier="<?php echo $n->notification_id ?>">&times;</button>
   <?php echo htmlentities($_SESSION['notification']['message']) ?>
  </div>
<?php $_SESSION['notification'] = false; endif; ?>
