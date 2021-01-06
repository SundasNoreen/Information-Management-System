-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 06, 2020 at 02:15 PM
-- Server version: 10.4.13-MariaDB
-- PHP Version: 7.2.32

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ims`
--

-- --------------------------------------------------------

--
-- Table structure for table `admins`
--

CREATE TABLE `admins` (
  `UserID` varchar(50) NOT NULL,
  `Name` text NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admins`
--

INSERT INTO `admins` (`UserID`, `Name`, `Phone`, `Password`) VALUES
('faizalatif@admin.ims', 'Faiza Latif', '03005874859', 'faiza'),
('mubashirhussain@admin.ims', 'Mubashir Hussain', '03452132345', 'mubashirhussain');

-- --------------------------------------------------------

--
-- Table structure for table `admin_details`
--

CREATE TABLE `admin_details` (
  `Name` text NOT NULL,
  `Phone` varchar(20) NOT NULL,
  `UserID` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin_details`
--

INSERT INTO `admin_details` (`Name`, `Phone`, `UserID`) VALUES
('Faiza Latif', '03005874859', 'faizalatif@admin.ims'),
('Mubashir Hussain', '03452132345', 'mubashirhussain@admin.ims');

-- --------------------------------------------------------

--
-- Table structure for table `available`
--

CREATE TABLE `available` (
  `Class` varchar(50) NOT NULL,
  `Semester` varchar(50) NOT NULL,
  `1` varchar(50) NOT NULL,
  `I1` varchar(50) NOT NULL,
  `2` varchar(50) NOT NULL,
  `I2` varchar(50) NOT NULL,
  `3` varchar(50) NOT NULL,
  `I3` varchar(50) NOT NULL,
  `4` varchar(50) NOT NULL,
  `I4` varchar(50) NOT NULL,
  `5` varchar(50) NOT NULL,
  `I5` varchar(50) NOT NULL,
  `6` varchar(50) NOT NULL,
  `I6` varchar(50) NOT NULL,
  `7` varchar(50) NOT NULL,
  `I7` varchar(50) NOT NULL,
  `8` varchar(50) NOT NULL,
  `I8` varchar(50) NOT NULL,
  `9` varchar(50) NOT NULL,
  `I9` varchar(50) NOT NULL,
  `10` varchar(50) NOT NULL,
  `I10` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `available`
--

INSERT INTO `available` (`Class`, `Semester`, `1`, `I1`, `2`, `I2`, `3`, `I3`, `4`, `I4`, `5`, `I5`, `6`, `I6`, `7`, `I7`, `8`, `I8`, `9`, `I9`, `10`, `I10`) VALUES
('CE-2019', 'Fall 2020', 'Introduction to Computing', 'Sadia Fatima', 'Electricity and Magnetism', 'Fawad Ali', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `classes`
--

CREATE TABLE `classes` (
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `classes`
--

INSERT INTO `classes` (`name`) VALUES
('CE-2019'),
('CE-2018'),
('CE-2016');

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE `courses` (
  `User_ID` varchar(50) NOT NULL,
  `Full_Name` text NOT NULL,
  `Course1` varchar(50) NOT NULL,
  `Session1` varchar(50) NOT NULL,
  `Course2` varchar(50) NOT NULL,
  `Session2` varchar(50) NOT NULL,
  `Course3` varchar(50) NOT NULL,
  `Session3` varchar(50) NOT NULL,
  `Course4` varchar(50) NOT NULL,
  `Session4` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`User_ID`, `Full_Name`, `Course1`, `Session1`, `Course2`, `Session2`, `Course3`, `Session3`, `Course4`, `Session4`) VALUES
('sadiafatima@teacher.ims', 'Sadia Fatima', 'Introduction to Computing', 'CE-2019', 'Programming Fundamentals', 'CE-2018', '', '', '', ''),
('fawadali@teacher.ims', 'Fawad Ali', 'Electricity and Magnetism', 'CE-2019', 'Digital and Logic Design', 'CE-2018', '', '', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `notify_students`
--

CREATE TABLE `notify_students` (
  `Date` timestamp NOT NULL DEFAULT current_timestamp(),
  `Heading` varchar(100) NOT NULL,
  `Message` varchar(9000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notify_students`
--

INSERT INTO `notify_students` (`Date`, `Heading`, `Message`) VALUES
('2020-09-04 17:59:12', 'Job Opportunities at Techlogix', '\r\nWe are looking to hire Application Consultants at Techlogix in following fields:\r\nElectrical Engineering (Minor Computer)\r\nComputer Engineering\r\nComputer Science\r\n \r\n\r\n'),
('2020-09-04 18:35:52', 'Profiles of CE-2019 and CE-2018 Updated', 'Assalam-u-Alikum Dear Students,\r\nYour Profiles are updated. View them at Student Portal.'),
('2020-09-04 19:00:06', 'Holidays of EidulFitar', 'Assalam-u-Alikum Dear Students,\r\nOn the occasion of Eid-ul-Fitar , Institution will remain closed for 5 days.'),
('2020-09-04 19:18:19', 'Internships', 'Internships at Engro are open.'),
('2020-09-05 18:50:45', 'Job Opportunity at Jazz Pakistan', 'Job opportunities for Computer Engineers at Jazz Pakistan. Drop your CVs at jobs.jazz.pk '),
('2020-09-05 19:18:56', 'Subjects updated', 'Dear Students,\r\nYour Subjects are updated. Kindly Register.'),
('2020-09-06 11:12:28', 'Fee of Month of September is Updated.', 'Dear Students,\r\nYour Fee for Month of September is updated.');

-- --------------------------------------------------------

--
-- Table structure for table `notify_teachers`
--

CREATE TABLE `notify_teachers` (
  `Date` timestamp NOT NULL DEFAULT current_timestamp(),
  `Heading` varchar(100) NOT NULL,
  `Message` varchar(9000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `notify_teachers`
--

INSERT INTO `notify_teachers` (`Date`, `Heading`, `Message`) VALUES
('2020-09-05 18:58:58', 'Salaries Updated', 'Salaries for the Month of September updated.'),
('2020-09-06 11:18:01', 'Subjects updated', 'Respected Teachers,\r\nYour Subjects are being updated.');

-- --------------------------------------------------------

--
-- Table structure for table `salary`
--

CREATE TABLE `salary` (
  `User_ID` varchar(50) NOT NULL,
  `Full_Name` text NOT NULL,
  `Teacher's Grade` int(2) NOT NULL,
  `Salary Details for the Year` int(4) NOT NULL,
  `1` int(11) NOT NULL,
  `2` int(11) NOT NULL,
  `3` int(11) NOT NULL,
  `April` int(11) NOT NULL,
  `May` int(11) NOT NULL,
  `June` int(11) NOT NULL,
  `July` int(11) NOT NULL,
  `August` int(11) NOT NULL,
  `September` int(11) NOT NULL,
  `October` int(11) NOT NULL,
  `November` int(11) NOT NULL,
  `December` int(11) NOT NULL,
  `Total Salary` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `salary`
--

INSERT INTO `salary` (`User_ID`, `Full_Name`, `Teacher's Grade`, `Salary Details for the Year`, `1`, `2`, `3`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November`, `December`, `Total Salary`) VALUES
('sadiafatima@teacher.ims', 'Sadia Fatima', 17, 2020, 0, 0, 0, 0, 0, 0, 0, 0, 100000, 90000, 0, 0, 0),
('fawadali@teacher.ims', 'Fawad Ali', 17, 2020, 0, 0, 0, 0, 0, 0, 0, 0, 100000, 90000, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `student-emails`
--

CREATE TABLE `student-emails` (
  `Registration_Number` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Class` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student-emails`
--

INSERT INTO `student-emails` (`Registration_Number`, `Email`, `Class`) VALUES
('2016-CE-01', 'noreensundas@gmail.com', 'CE-2016'),
('2018-CE-01', 'noreensundas@gmail.com', 'CE-2018'),
('2018-CE-02', 'noreensundas@gmail.com', 'CE-2018'),
('2018-CE-03', 'noreensundas@gmail.com', 'CE-2018'),
('2018-CE-04', 'noreensundas@gmail.com', 'CE-2018'),
('2018-CE-06', 'noreensundas@gmail.com', 'CE-2018'),
('2019-CE-01', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-02', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-03', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-04', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-05', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-06', 'noreensundas@gmail.com', 'CE-2019'),
('2019-CE-07', 'noreensundas@gmail.com', 'CE-2019');

-- --------------------------------------------------------

--
-- Table structure for table `student-lgins`
--

CREATE TABLE `student-lgins` (
  `Class` varchar(50) NOT NULL,
  `User_ID` varchar(50) NOT NULL,
  `Password` varchar(50) NOT NULL,
  `Reg` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student-lgins`
--

INSERT INTO `student-lgins` (`Class`, `User_ID`, `Password`, `Reg`) VALUES
('CE-2016', '2016ce01@student.ims', 'hiraaslam', '2016-CE-01'),
('CE-2018', '2018ce01@student.ims', 'sidrasoniaaziz', '2018-CE-01'),
('CE-2018', '2018ce02@student.ims', 'amnajamshaid', '2018-CE-02'),
('CE-2018', '2018ce03@student.ims', 'sayedaasma', '2018-CE-03'),
('CE-2018', '2018ce06@student.ims', 'maryamnasir', '2018-CE-06'),
('CE-2019', '2019ce01@student.ims', 'alinaqikhan', '2019-CE-01'),
('CE-2019', '2019ce02@student.ims', 'abdulmueez', '2019-CE-02'),
('CE-2019', '2019ce03@student.ims', 'sundasnoreen', '2019-CE-03'),
('CE-2019', '2019ce04@student.ims', 'saba', '2019-CE-04'),
('CE-2019', '2019ce05@student.ims', 'tayyabaasif', '2019-CE-05'),
('CE-2019', '2019ce06@student.ims', 'azanamir', '2019-CE-06'),
('CE-2019', '2019ce07@student.ims', 'aqsaayaz', '2019-CE-07');

-- --------------------------------------------------------

--
-- Table structure for table `students-dues`
--

CREATE TABLE `students-dues` (
  `Class` varchar(50) NOT NULL,
  `Registration_Number` varchar(50) NOT NULL,
  `Name` text NOT NULL,
  `Amount Paid till Now` int(10) NOT NULL,
  `Dues_Left` int(10) NOT NULL,
  `Total Amout Paid` int(10) NOT NULL,
  `Remarks` text NOT NULL,
  `Is Paid?` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `students-dues`
--

INSERT INTO `students-dues` (`Class`, `Registration_Number`, `Name`, `Amount Paid till Now`, `Dues_Left`, `Total Amout Paid`, `Remarks`, `Is Paid?`) VALUES
('CE-2016', '2016-CE-01', 'Hira Aslam', 200000, 40000, 200000, 'Month of September.', ''),
('CE-2018', '2018-CE-01', 'Sidra Sonia Aziz', 150000, 30000, 150000, 'Fee of Month of September.', ''),
('CE-2018', '2018-CE-02', 'Amna Jamshaid', 150000, 30000, 150000, 'Fee of Month of September.', ''),
('CE-2018', '2018-CE-03', 'Sayeda Asma', 150000, 30000, 150000, 'Fee of Month of September.', ''),
('CE-2018', '2018-CE-04', 'Tanjeena', 150000, 30000, 150000, 'Fee of Month of September.', ''),
('CE-2018', '2018-CE-06', 'Maryam Nasir', 200000, 40000, 200000, 'Fee of Month of November.', ''),
('CE-2019', '2019-CE-01', 'Ali Naqi Khan', 170000, 0, 170000, 'Month of September is Cleared.', ''),
('CE-2019', '2019-CE-02', 'Abdul Mueez', 170000, 0, 170000, 'Month of September is Cleared.', ''),
('CE-2019', '2019-CE-03', 'Sundas Noreen', 170000, 0, 170000, 'Month of September is Cleared.', ''),
('CE-2019', '2019-CE-04', 'Saba', 170000, 0, 170000, 'Month of September is Cleared.', ''),
('CE-2019', '2019-CE-05', 'Tayyaba Asif', 170000, 0, 170000, 'Month of September is Cleared.', ''),
('CE-2019', '2019-CE-06', 'Azan Amir', 130000, 40000, 130000, 'Month of September.', ''),
('CE-2019', '2019-CE-07', 'Aqsa Ayaz', 130000, 40000, 130000, 'Month of September.', '');

-- --------------------------------------------------------

--
-- Table structure for table `students_personal`
--

CREATE TABLE `students_personal` (
  `Class` varchar(50) NOT NULL,
  `Name` text NOT NULL,
  `Registration_Number` varchar(50) NOT NULL,
  `Father_Name` text NOT NULL,
  `Date_of_Birth` date NOT NULL,
  `Gender` varchar(20) NOT NULL,
  `District` text NOT NULL,
  `Address` varchar(200) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `CNIC` varchar(15) NOT NULL,
  `Email ID` varchar(50) NOT NULL,
  `Is-host` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `students_personal`
--

INSERT INTO `students_personal` (`Class`, `Name`, `Registration_Number`, `Father_Name`, `Date_of_Birth`, `Gender`, `District`, `Address`, `Phone`, `CNIC`, `Email ID`, `Is-host`) VALUES
('CE-2016', 'Hira Aslam', '2016-CE-01', 'Muhammad Aslam', '2001-10-03', 'Female', 'Lahore', 'GT Road, Lahore', '03094560417', '21345-6754321-9', 'noreensundas@gmail.com', 'No'),
('CE-2018', 'Sidra Sonia Aziz', '2018-CE-01', 'Aziz Ahmad', '2002-01-01', 'Female', 'Okara', 'Gulshan Iqbal, Okara', '03094560417', '32456-9876549-8', 'noreensundas@gmail.com', 'Yes'),
('CE-2018', 'Amna Jamshaid', '2018-CE-02', 'Muhammad jamshaid', '2001-07-04', 'Female', 'Gunjrawala', 'Gunjrawala Cantt', '03214521248', '32456-9876549-8', 'noreensundas@gmail.com', 'Yes'),
('CE-2018', 'Sayeda Asma', '2018-CE-03', 'Anwar Ali', '2001-10-17', 'Female', 'Lahore', 'Iqbal Town, Lahore', '03214521248', '34563-3214567-8', 'noreensundas@gmail.com', 'No'),
('CE-2018', 'Tanjeena', '2018-CE-04', 'Zubair', '2001-12-07', 'Female', 'Lahore', 'Iqbal Town, Lahore', '03214521248', '34563-3214567-8', 'noreensundas@gmail.com', 'No'),
('CE-2018', 'Maryam Nasir', '2018-CE-06', 'Nasir Suleman', '2001-03-08', 'Female', 'Lahore', 'Iqbal Town, Lahore', '03214521248', '21345-6754321-9', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Ali Naqi Khan', '2019-CE-01', 'Ali Mohsin Khan', '2002-11-11', 'Male', 'Lahore', 'Mughalpura, Lahore', '03214251522', '12589-3014785-9', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Abdul Mueez', '2019-CE-02', 'Manan Rashid', '2001-12-14', 'Male', 'Lahore', 'GT Road, Lahore', '03094560417', '12589-3014785-9', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Sundas Noreen', '2019-CE-03', 'Waheed Akhtar', '2001-11-20', 'Female', 'Bahawalnagar', 'Multan Cantt', '03256938741', '12589-3014785-9', 'noreensundas@gmail.com', 'Yes'),
('CE-2019', 'Saba', '2019-CE-04', 'Saeed', '2001-12-18', 'Female', 'Lahore', 'Gulshan e Ravi, Lahore', '03256938741', '36592-9854763-2', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Tayyaba Asif', '2019-CE-05', 'Asif', '2001-03-02', 'Female', 'Lahore', 'Wapda Town, Lahore', '03094560417', '74125-9887450-9', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Azan Amir', '2019-CE-06', 'Amir', '2001-05-22', 'Male', 'Lahore', 'Model Town, Lahore', '032185479632', '74125-9887450-9', 'noreensundas@gmail.com', 'No'),
('CE-2019', 'Aqsa Ayaz', '2019-CE-07', 'Ayaz Rao', '1999-01-04', 'Female', 'Bahawalpur', 'Islamia Colony, Bahawalpur', '03214521248', '32456-9876549-8', 'noreensundas@gmail.com', 'Yes');

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `Class` varchar(50) NOT NULL,
  `Registration_Number` varchar(50) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `1` varchar(50) NOT NULL,
  `2` varchar(50) NOT NULL,
  `3` varchar(50) NOT NULL,
  `4` varchar(50) NOT NULL,
  `5` varchar(50) NOT NULL,
  `6` varchar(50) NOT NULL,
  `7` varchar(50) NOT NULL,
  `8` varchar(50) NOT NULL,
  `9` varchar(50) NOT NULL,
  `10` varchar(50) NOT NULL,
  `11` varchar(50) NOT NULL,
  `12` varchar(50) NOT NULL,
  `13` varchar(50) NOT NULL,
  `14` varchar(50) NOT NULL,
  `15` varchar(50) NOT NULL,
  `16` varchar(50) NOT NULL,
  `17` varchar(50) NOT NULL,
  `18` varchar(50) NOT NULL,
  `19` varchar(50) NOT NULL,
  `20` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`Class`, `Registration_Number`, `Name`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`, `10`, `11`, `12`, `13`, `14`, `15`, `16`, `17`, `18`, `19`, `20`) VALUES
('CE-2016', '2016-CE-01', 'Hira Aslam', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2018', '2018-CE-01', 'Sidra Sonia Aziz', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2018', '2018-CE-02', 'Amna Jamshaid', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2018', '2018-CE-03', 'Sayeda Asma', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2018', '2018-CE-04', 'Tanjeena', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2018', '2018-CE-06', 'Maryam Nasir', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-01', 'Ali Naqi Khan', 'Introduction to Computing', 'A+', 'Electricity and Magnetism', 'B+', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-02', 'Abdul Mueez', 'Introduction to Computing', 'A+', 'Electricity and Magnetism', 'B+', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-03', 'Sundas Noreen', 'Programming Fundamentals', '0', 'Electricity and Magnetism', 'B+', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-04', 'Saba', 'Introduction to Computing', 'A', 'Electricity and Magnetism', 'B+', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-05', 'Tayyaba Asif', 'Introduction to Computing', 'A', 'Electricity and Magnetism', 'B', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-06', 'Azan Amir', 'Introduction to Computing', 'A', 'Electricity and Magnetism', 'B', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'),
('CE-2019', '2019-CE-07', 'Aqsa Ayaz', 'Introduction to Computing', 'A', 'Electricity and Magnetism', 'B', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0');

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `User_ID` varchar(50) NOT NULL,
  `Full_Name` text NOT NULL,
  `Father/Husband Name` text NOT NULL,
  `CNIC` varchar(15) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Grade` int(2) NOT NULL,
  `Qualification` text NOT NULL,
  `Contact` varchar(15) NOT NULL,
  `Address` text NOT NULL,
  `JoiningDate` varchar(20) NOT NULL,
  `password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`User_ID`, `Full_Name`, `Father/Husband Name`, `CNIC`, `Email`, `Grade`, `Qualification`, `Contact`, `Address`, `JoiningDate`, `password`) VALUES
('fawadali@teacher.ims', 'Fawad Ali', 'Ali Mehmood', '23454-09876524-', 'noreensundas@gmail.com', 17, 'PhD Physics', '03224567856', 'Gulshan Johar, Lahore', 'Aug 2020', 'fawad'),
('sadiafatima@teacher.ims', 'Sadia Fatima', 'Muhammad Ali', '34556-0987190-2', 'sundasnoreen0@gmail.com', 17, 'PhD Electrical Engineering', '03224567856', 'Gulshan Johar, Lahore', 'Aug 2020', 'sadia');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admins`
--
ALTER TABLE `admins`
  ADD PRIMARY KEY (`UserID`);

--
-- Indexes for table `student-emails`
--
ALTER TABLE `student-emails`
  ADD PRIMARY KEY (`Registration_Number`);

--
-- Indexes for table `student-lgins`
--
ALTER TABLE `student-lgins`
  ADD PRIMARY KEY (`Reg`);

--
-- Indexes for table `students-dues`
--
ALTER TABLE `students-dues`
  ADD PRIMARY KEY (`Registration_Number`);

--
-- Indexes for table `students_personal`
--
ALTER TABLE `students_personal`
  ADD PRIMARY KEY (`Registration_Number`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`Registration_Number`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`User_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
