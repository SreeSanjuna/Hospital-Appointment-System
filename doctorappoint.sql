create database doctorappoint;
use doctorappoint;
-- drop database doctorappoint;

create table patient_details (
  patientID int primary key auto_increment,
  fullname varchar(255),
  emailid varchar(255) unique,
  gender varchar(255),
  dob date,
  pwd varchar(255),
  contactno int,
  address varchar(255),
  state varchar(255),
  city varchar(255)
);



create table specialization(
  sid int primary key auto_increment,
  sname varchar(255) unique
);


create table doctor_details(
  doctorID int primary key auto_increment,
  fullname varchar(255),
  qualification varchar(255),
  emailid varchar(255) unique,
  contactno int,
  consultancyfee varchar(255),
  pwd varchar(255),
  address varchar(255),
  city varchar(255),
  state varchar(255)
);


create table doctor_session(
  sessionID int primary key auto_increment,
  doctorID int,
  login_time datetime,
  logout_time datetime,
  foreign key (doctorID) references doctor_details(doctorID)
);

create table D_S_Mapping (
sid int,
doctorID int,
foreign key (sid) references specialization(sid),
foreign key (doctorID) references doctor_details(doctorID)
);

create table appointments(
  aid int primary key auto_increment,
  patientID int,
  doctorID int,
  a_date date,
  a_time time,
  reason varchar(255),
  astatus varchar(255) default 'pending',
  foreign key (patientID) references patient_details(patientID),
  foreign key (doctorID) references doctor_details(doctorID)
);

select * from doctor_details order by doctorID desc;

insert into specialization (sname) values ('Allergist/Immunologist'), ('Anesthesiologist'),('Cardiologist'),
('Dermatologist'),('Endocrinologist'),('Emergency Physician'),('Gastroenterologist'),('Gynaecologist/Obstetrician'),
('General Surgeon'),('Hematologist'),('Nephrologist'),('Neurologist'),('Oncologist'),('Ophthalmologist'),('Orthopedist'),
('Otolaryngologist \(ENT\)'),('Pediatrician'),('Physiatrist'),('Podiatrist'),('Psychiatrist'),('Pulmonologist'),
('Rheumatologist'),('Urologist');

-- select * from specialization; 

-- delete from specialization where sid=11;

-- select pwd from doctor_details where emailid='your.email+fakedata28488@gmail.com';

-- insert into d_s_mapping values ((select doctorID from doctor_details where emailid='your.email+fakedata28488@gmail.com'),1);
-- select * from d_s_mapping;
-- delete from d_s_mapping where sid=2;