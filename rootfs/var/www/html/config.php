<?php

$db = new SQLite3("/config/db/openhr20.sqlite");
$TIMEZONE="Europe/Berlin";
$RRD_ENABLE=false;
$PLOTS_DIR = "plots";
$RRD_DAYS = array (3, 7, 30, 90);



  // translation table for valve names
  // example:
$room_name = array (
    0x10 => 'Werkstatt',
    0x11 => 'Waschküche',
    0x12 => 'Wäschekammer',
    0x13 => 'Treppenhaus',
    0x0C => 'Gästeklo',
    0x01 => 'Büro neu',
    0x02 => 'Bad unten',
    0x03 => 'Küche',
    0x04 => 'EZ1',
    0x05 => 'EZ2',
    0x06 => 'WZ1',
    0x07 => 'WZ2',
    0x08 => 'WZ3',
    0x09 => 'Bad oben',
    0x0A => 'Sabine',
    0x0B => 'Jürgen',
    0x0D => 'Küche oben', // default setting in valves
    0x0E => 'SZ1',
    0x0F => 'SZ2'
  //  0x0b => 'salon', // default setting in valves
   // 0x0c => 'dzieciecy', // default setting in valves
  ); 

/*  $room_name = array (
    0x11 => 'decak',
    0x12 => 'obyvak',
    0x13 => 'loznice',
    0x14 => 'kuchyne',
    0x15 => 'koupelna'
  );
*/

  // translation table for timers name (weekdays)
  $timer_names =  array (
    'Week',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Sunday'
  );
  /*$timer_names =  array (
    'tyden',
    'pondeli',
    'utery',
    'streda',
    'ctvrtek',
    'patek',
    'sobota',
    'nedele'
  );
*/

  // symbols for 4 temperature mode
  // unicode version with nice moon/sun symbols, have problem on mobile Opera browser
  
   $symbols = array (
      'x',		//off
      '&#x263e;',	//Night
      '&#x2600;',	//Day
      '&#x263c;'	//Comfort
    ); 

  // universal symbols, but not nice // english
  /* $symbols = array (
      'off',
      'Night',
      'Day',
      '+++' 		//Comfort
  ); */

/*  $symbols = array (
      'off',
      'Noc',
      'Den',
      '+++'
  );
*/

  $refresh_value=15; // refresh time for command queue pending wait 

  $chart_hours = 48; // chart contain values from last 12 hours

  $warning_age = 8*60; // maximum data age for warning

  $error_age = 20*60; // maximum data age for error
  
