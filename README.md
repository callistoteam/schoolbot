# schoolbot

> A discord bot that informs the school's academic calendar, timetable, and meals in Republic of Korea

[![GitHub license](https://img.shields.io/github/license/callistoteam/schoolbot)](https://github.com/callistoteam/schoolbot/blob/master/LICENSE)
[![Python application](https://github.com/callistoteam/schoolbot/workflows/Python%20application/badge.svg)](https://github.com/callistoteam/schoolbot/actions?query=workflow%3A%22Python+application%22)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

## Pre-rendered meal image API

If you want to use this API, contact to `매리#4633` by discord.

## Database Structure

### Table `users`
|Name|Type|Description|Default|
|---|----|-----------|---|
|id|BIGINT(18)|Discord id of user||
|neis_ae|VARCHAR(3)|Neis educational office code||
|neis_se|VARCHAR(7)|Neis school code||
|iamschool|VARCHAR(5)|Neis school code|0|
|public|TINYINT(1)|whether profile public or not|1|
|grade|INT(1)|grade setting||
|class_nm|INT(2)|class name||
|class|VARCHAR(3)|class||
