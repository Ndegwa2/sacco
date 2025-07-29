<?php
/**
 * Adminer - Database management tool for PostgreSQL
 * Download adminer.php from https://www.adminer.org/
 * Place this file in your web server directory
 */

// Download Adminer
if (!file_exists('adminer.php')) {
    echo "Downloading Adminer...\n";
    file_put_contents('adminer.php', file_get_contents('https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1.php'));
}

// Include Adminer
include 'adminer.php';
?>