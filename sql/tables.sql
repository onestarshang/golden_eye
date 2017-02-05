# 数据表

CREATE TABLE `sz399300_minute` (
  `datetime` datetime NOT NULL,
  `open` float(10,6) NOT NULL,
  `high` float(10,6) NOT NULL,
  `low` float(10,6) NOT NULL,
  `close` float(10,6) NOT NULL,
  `volume` int(11) NOT NULL,
  `turnover` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


LOAD DATA INFILE 'scripts/sz_minute.csv' INTO TABLE sz399300_minute FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n' IGNORE 1 ROWS;
