create database project ;
use project;

CREATE TABLE Explore_movies (
   Movie_ID  INT NOT NULL,
   Movie_title  VARCHAR(45) NOT NULL,
   Movie_Genre  VARCHAR(10) NOT NULL,
   Movie_release_date  DATETIME NOT NULL,
   Movie_director  VARCHAR(45) NOT NULL,
   Movie_earning  FLOAT NULL,
   Movie_actor  VARCHAR(45)NOT NULL,
   Rating_review_Movie_ID  INT NOT NULL,
  PRIMARY KEY ( Movie_ID )
  );

CREATE TABLE Rating_review (
  Movie_ID INT NOT NULL,
  Movie_user_rating INT NOT NULL,
  Movie_imdb_rating INT NOT NULL,
  PRIMARY KEY (Movie_ID),
    FOREIGN KEY (Movie_ID)
    REFERENCES Explore_movies(Movie_ID)
 );



    
CREATE TABLE Already_watched  (
   Movie_ID  INT NOT NULL,
   Movie_title  VARCHAR(45) UNIQUE,
   Movie_genre  VARCHAR(10) NOT NULL,
   Movie_release_date  DATETIME NOT NULL,
   Movie_rating  INT NOT NULL,
  PRIMARY KEY ( Movie_ID )
);

                                                                                                               
CREATE TABLE To_watch  (
   Movie_ID  INT NOT NULL,
   Movie_title  VARCHAR(45) UNIQUE,
   Movie_genre  VARCHAR(10) NOT NULL,
   Movie_release_date  DATETIME NOT NULL,
   Movie_rating  INT NOT NULL,
  PRIMARY KEY ( Movie_ID )
); 
                                                                                                               
                                                                                                               
CREATE TABLE Currently_watching  (
   Movie_ID  INT NOT NULL,
   Movie_title  VARCHAR(45) NOT NULL,
   Movie_genre  VARCHAR(10) NOT NULL,
   Movie_release_date  DATETIME NOT NULL,
   Movie_rating  INT NOT NULL,
  PRIMARY KEY ( Movie_ID )
);
                                                                        
CREATE TABLE User_account  (
   User_id  INT NOT NULL,
   User_name  VARCHAR(45) UNIQUE,
   User_password  VARCHAR(45) NOT NULL,
   User_bio  VARCHAR(100) NOT NULL,
  PRIMARY KEY ( User_id)
);

insert into to_watch (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('2','3 idiots','comedy','1999-03-11','8.1');
insert into to_watch (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('3','knives out','mystery','2019-11-21','8.7');

update to_watch set movie_rating=7 where movie_genre='Sci-fi';

delete from to_watch where movie_rating='8';

start transaction;
update to_watch set Movie_title='knives out 2' where Movie_ID='3';
rollback;

select count(*)as number_of_movies from to_watch;
select * from to_watch order by Movie_title desc;
alter table to_watch modify column Movie_rating float(10);
insert into to_watch (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('4','searching','mystery','2018-06-21','7.6'),
('5','rush hour','action','1998-09-17','6.7'),
( '6','hera pheri','comedy','2000-03-31','8.2'),
('7','interstellar','Sci-fi','2014-11-07','8.7');
select * from to_watch;
select * from to_watch where Movie_rating <9 and  Movie_title like "%r";
select Movie_genre,count(movie_title) from to_watch group by Movie_genre;

alter table already_watched modify column Movie_rating float(10);
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('1','3 Idiots','comedy','1999-03-11','8.1');
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('2','Knives out','mystery','2019-11-21','8.7');
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('3','Interstellar','Sci-fi','2014-11-07','8.7');
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('4','Dune','Sci-fi','2024-03-15','8.0');
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('5','Your name','Romance','2017-04-07','8.8');
insert into already_watched (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('6','How to Train Your Dragon','Fantasy','2010-04-16','8.1');

select * from already_watched;
update already_watched set Movie_rating=8.1 where Movie_ID=1;
update already_watched set Movie_rating=8.7 where Movie_ID=2;
update already_watched set Movie_rating=8.7 where Movie_ID=3;
update already_watched set Movie_rating=8.0 where Movie_ID=4;
update already_watched set Movie_rating=8.8 where Movie_ID=5;
update already_watched set Movie_rating=8.1 where Movie_ID=6;
select * from already_watched;

select * from already_watched inner join to_watch on already_watched.Movie_title=to_watch.Movie_title;
select * from already_watched left join to_watch on already_watched.Movie_title=to_watch.Movie_title;
select * from already_watched right join to_watch on already_watched.Movie_genre=to_watch.Movie_genre;
select * from already_watched union select * from to_watch;
select * from already_watched intersect select * from to_watch;
select * from already_watched except select * from to_watch;

alter table currently_watching modify column Movie_rating float(10);
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('1','Bullet train','Action','2022-08-05','7.3');
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('2','Fight club','Thriller','1999-10-15','8.8');
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('3','The conjuring','Horror','2013-08-02','7.5');
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('4','Scary Movie','Comedy','2013-08-02','6.3');
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('5','The karate kid','Teen drama','2010-07-11','6.2');
insert into currently_watching (Movie_ID,movie_title,Movie_genre,Movie_release_date,Movie_rating) values ('6','Kabhi khushi kabhi gham','Musical','2001-12-14','7.4');

select max(Movie_rating)
from currently_watching;

select min(Movie_rating)
from currently_watching;

select avg(Movie_rating) from currently_watching;

select * from to_watch;

 select mid(Movie_title,2,3) from currently_watching;
 select round(Movie_rating,2) from to_watch;
 
 select Movie_genre from to_watch group by Movie_genre having avg(Movie_rating)>7.2;
 
select sum(Movie_rating) from currently_watching;

select movie_id,now() as date_and_time from already_watched;

select Movie_title,length(Movie_title) from currently_watching;
