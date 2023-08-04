DROP DATABASE IF EXISTS guardsman_timesheet;
CREATE DATABASE guardsman_timesheet;
USE guardsman_timesheet;

DROP TABLE IF EXISTS work_hours;
CREATE TABLE work_hours (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date DATE DEFAULT (current_date) NOT NULL,
  punch_in DATETIME NOT NULL,
  punch_out DATETIME DEFAULT NULL
);

DROP VIEW IF EXISTS time_sheet;
CREATE VIEW time_sheet AS
SELECT
  id,
  date,
  TIME(punch_in) AS punch_in_time,
  TIME(punch_out) AS punch_out_time
FROM work_hours;

DROP VIEW IF EXISTS daily_hours;
CREATE VIEW daily_hours AS
SELECT
    DATE(date) AS day,
    CONCAT(
        SUM(
            TIMESTAMPDIFF(
                HOUR,
                punch_in,
                IFNULL(punch_out, NOW())
            )
        ),
        'h ',
        SUM(
            TIMESTAMPDIFF(
                MINUTE,
                punch_in,
                IFNULL(punch_out, NOW())
            )
        ) % 60,
        'm'
    ) AS total_hours
FROM
    work_hours
GROUP BY
    day
ORDER BY
    day DESC;

DROP VIEW IF EXISTS weekly_hours;
CREATE VIEW weekly_hours AS
SELECT
    -- previous week Sunday as week start
    DATE_SUB(date, INTERVAL (DAYOFWEEK(date) - 1) DAY) AS week_start,
    CONCAT(
        FLOOR(
            SUM(
                TIMESTAMPDIFF(
                    MINUTE,
                    punch_in,
                    IFNULL(punch_out, NOW())
                )
            ) / 60
        ),
        'h ',
        SUM(
            TIMESTAMPDIFF(
                MINUTE,
                punch_in,
                IFNULL(punch_out, NOW())
            )
        ) % 60,
        'm'
    ) AS total_hours
FROM
    work_hours
GROUP BY
    week_start;


/*
SELECT * FROM work_hours;
SELECT * FROM time_sheet;
SELECT * FROM daily_hours;
SELECT * FROM weekly_hours;
*/