-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 25, 2024 at 03:45 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `python_sales`
--

-- --------------------------------------------------------

--
-- Table structure for table `cart`
--

CREATE TABLE `cart` (
  `cart_id` int(11) NOT NULL,
  `customer_name` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `price` double(40,2) NOT NULL,
  `quantity` int(255) NOT NULL,
  `total` double(40,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `cart`
--

INSERT INTO `cart` (`cart_id`, `customer_name`, `product_name`, `price`, `quantity`, `total`) VALUES
(1, 'asd', 'NSIC RC 520', 1500.00, 1, 1500.00),
(2, 'asd', 'RC 160', 1500.00, 2, 3000.00);

-- --------------------------------------------------------

--
-- Table structure for table `product`
--

CREATE TABLE `product` (
  `product_id` int(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(255) NOT NULL,
  `price` double(40,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `product`
--

INSERT INTO `product` (`product_id`, `product_name`, `quantity`, `price`) VALUES
(8, 'RC 160', 4, 1500.00),
(9, 'NSIC RC 520', 12, 1500.00),
(10, 'PSB RC30', 6, 1090.00),
(11, 'NSIC RC 200H', 10, 1520.00),
(14, 'PSB RC 3009', 4, 1020.00),
(15, 'NSIC RC 800', 0, 1350.00),
(25, 'ab-4753765', 5, 1240.00),
(26, 'jdfc=3y2u', 6, 1250.00),
(27, 'sdsjf-3434', 6, 1270.00);

-- --------------------------------------------------------

--
-- Table structure for table `report`
--

CREATE TABLE `report` (
  `report_id` int(11) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `customer_name` varchar(255) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `quantity` int(255) NOT NULL,
  `price` double(40,2) NOT NULL,
  `total` double(40,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `report`
--

INSERT INTO `report` (`report_id`, `date`, `customer_name`, `product_name`, `quantity`, `price`, `total`) VALUES
(1, '2024-01-20', 'neil', 'NSIC RC 520', 1, 1500.00, 1500.00),
(2, '2024-01-20', 'juan', 'NSIC RC 800', 2, 1350.00, 2700.00),
(3, '2024-01-20', 'juan', 'PSB RC 3009', 1, 1020.00, 1020.00),
(4, '2024-01-27', 'vic', 'NSIC RC 520', 1, 1500.00, 1500.00),
(5, '2024-02-10', 'may', 'NSIC RC 200H', 1, 1520.00, 1520.00),
(6, '2024-02-18', 'ai', 'NSIC RC 520', 1, 1500.00, 1500.00),
(7, '2024-02-18', 'juan', 'PSB RC30', 1, 1090.00, 1090.00),
(8, '2024-02-18', 'Robert', 'NSIC RC 800', 1, 1350.00, 1350.00),
(9, '2024-03-18', 'Un', 'RC 160', 1, 1500.00, 1500.00),
(10, '2024-03-18', 'qwe', 'PSB RC 3009', 2, 1020.00, 2040.00),
(11, '2024-03-18', 'Kei', 'NSIC RC 520', 1, 1500.00, 1500.00),
(12, '2024-03-18', 'Kei', 'NSIC RC 520', 1, 1500.00, 1500.00),
(13, '2024-04-18', 'Ab', 'RC 160', 2, 1500.00, 3000.00),
(14, '2024-04-18', 'Rud', 'NSIC RC 800', 1, 1350.00, 1350.00),
(15, '2024-05-23', 'Ad', 'RC 160', 1, 1500.00, 1500.00),
(16, '2024-05-23', 'Ad', '3893-535', 2, 1000.00, 2000.00),
(17, '2024-05-23', 'Ad', 'NSIC RC 520', 1, 1500.00, 1500.00),
(18, '2024-05-25', 'nic', 'RC 160', 1, 1500.00, 1500.00),
(19, '2024-05-25', 'nic', 'NSIC RC 200H', 2, 1520.00, 3040.00),
(26, '2024-05-25', 'qwe', 'NSIC RC 520', 2, 1500.00, 3000.00),
(27, '2024-05-25', 'qwe', 'RC 160', 2, 1500.00, 3000.00);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `user_type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `name`, `username`, `password`, `user_type`) VALUES
(1, 'admin', 'admin', 'admin', 'admin'),
(2, 'cashier', 'cashier', 'cashier', 'cashier'),
(10, 'Rb', 'rw2', 'r', 'cashier');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`cart_id`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `report`
--
ALTER TABLE `report`
  ADD PRIMARY KEY (`report_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `cart`
--
ALTER TABLE `cart`
  MODIFY `cart_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `product`
--
ALTER TABLE `product`
  MODIFY `product_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `report`
--
ALTER TABLE `report`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
