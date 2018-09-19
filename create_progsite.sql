drop database if exists progsite;
create database progsite;
create user if not exists siteuser@localhost identified by 'sitepass';
grant all on progsite.* to siteuser@localhost;
