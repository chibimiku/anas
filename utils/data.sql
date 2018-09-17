CREATE TABLE `fetch_list` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`url` VARCHAR(255) NOT NULL,
	`fetchset` VARCHAR(255) NOT NULL DEFAULT 'default',
	`status` TINYINT(4) NOT NULL DEFAULT '',
	`local_path` VARCHAR(255) NOT NULL DEFAULT '',
	`init_timestamp` TIMESTAMP NOT NULL DEFAULT '',
	`fetch_timestamp` INT(11) NOT NULL DEFAULT '0',
	`remote_id` INT(11) NOT NULL DEFAULT '0',
	`title` VARCHAR(255) NOT NULL DEFAULT '',
	`author_name` VARCHAR(255) NOT NULL DEFAULT '',
	`author_id` BIGINT(20) NOT NULL DEFAULT '0',
	`comment` TEXT NULL DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE INDEX `url` (`url`),
	INDEX `fetchset` (`fetchset`),
	INDEX `status` (`status`),
	INDEX `author_id` (`author_id`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
AUTO_INCREMENT=0
;

CREATE TABLE `gallerys` (
	`gid` INT(11) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL,
	`count` INT(11) NOT NULL DEFAULT '0',
	`author` VARCHAR(255) NOT NULL,
	`local_dir` VARCHAR(255) NOT NULL,
	`remote_dir` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`gid`),
	INDEX `author` (`author`),
	INDEX `name` (`name`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;


CREATE TABLE `gallerys_image` (
	`imageid` INT(11) NOT NULL AUTO_INCREMENT,
	`gid` INT(11) NOT NULL DEFAULT '0',
	`display_order` INT(11) NOT NULL DEFAULT '0',
	`filename` VARCHAR(50) NOT NULL,
	PRIMARY KEY (`imageid`),
	INDEX `gid` (`gid`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
;


CREATE TABLE `titles` (
	`log_id` INT(11) NOT NULL AUTO_INCREMENT,
	`url` VARCHAR(255) NOT NULL,
	`title` VARCHAR(255) NOT NULL,
	PRIMARY KEY (`log_id`)
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM
AUTO_INCREMENT=5
;

