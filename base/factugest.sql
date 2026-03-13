-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 13-03-2026 a las 19:13:20
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `factugest`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `cod_cliente` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `tipo_documento` varchar(255) DEFAULT NULL,
  `numero_documento` varchar(255) DEFAULT NULL,
  `telefono` varchar(255) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`cod_cliente`, `nombre`, `tipo_documento`, `numero_documento`, `telefono`, `correo`, `direccion`) VALUES
(2, 'juan perez', 'V', '12345678', '0412-1234567', 'juan@email.com', 'caracas, venezuela'),
(3, 'María García', 'V', '87654321', '0414-7654321', 'maria@email.com', 'Valencia, Venezuela'),
(6, 'Diana', 'J', '1005066451', '3107093720', 'diana@gmail.com', 'av10a');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `configuracion`
--

CREATE TABLE `configuracion` (
  `clave` varchar(255) NOT NULL,
  `valor` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `document_type` char(1) NOT NULL COMMENT 'C for National ID, E for Foreign ID',
  `document_number` varchar(20) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `ciudad` varchar(50) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `pais` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `customers`
--

INSERT INTO `customers` (`customer_id`, `full_name`, `document_type`, `document_number`, `phone`, `email`, `address`, `ciudad`, `departamento`, `pais`) VALUES
(1, 'Consumidor Final', 'C', '222222222222', '', '', '', '', '', ''),
(2, 'Maria Fernanda Ruiz', 'C', '1015432109', '3209876543', 'mafe.ruiz@outlook.com', 'Libertadores Ave # 11-45', '', '', ''),
(3, 'Juan Sebastian Gomez', 'E', 'E87654321', '3156789012', 'juan.gomez@gmail.com', 'La Playa Neighborhood, House 4', '', '', ''),
(4, 'Diana Marcela Rojas', 'C', '1093456789', '3004567890', 'diana.rojas@servicios.co', '7N St # 3-12, Los Patios', '', '', ''),
(5, 'Ricardo Jose Torres', 'C', '1116789456', '3112345678', 'ricardo.torres@empresa.com', '0 Avenue # 15-30', '', '', ''),
(6, 'Elena Patricia Meza', 'C', '1012345987', '3189012345', 'elena.meza@misena.edu.co', 'Siglo XXI Estate', '', '', ''),
(7, 'Oscar David Ortiz', 'E', 'E12345678', '3145678234', 'oscar.ortiz@flete.net', 'Industrial Zone, Plot 5', '', '', ''),
(8, 'Sandra Milena Cano', 'C', '1090123456', '3216540987', 'sandra.cano@yahoo.es', '24th St # 12-05, Villa del Rosario', '', '', ''),
(9, 'Luis Alberto Quintero', 'C', '1115678234', '3124567890', 'luis.quintero@tecnicos.com', '5th Ave # 10-10', '', '', ''),
(10, 'Angela Maria Velez', 'C', '1018907654', '3012345678', 'angela.velez@estudio.edu', '15th St # 4-50, Atalaya', '', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `descuentos`
--

CREATE TABLE `descuentos` (
  `cod_descuento` int(11) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `porcentaje` double NOT NULL,
  `aplica_a_producto` smallint(6) NOT NULL,
  `aplica_a_factura` smallint(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `descuentos`
--

INSERT INTO `descuentos` (`cod_descuento`, `descripcion`, `porcentaje`, `aplica_a_producto`, `aplica_a_factura`) VALUES
(55501, 'Seasonal Discount', 10, 1, 0),
(55502, 'Frequent Customer Promotion', 5, 0, 1),
(55503, 'End of Month Offer', 15, 0, 1),
(55504, 'Volume Discount', 8, 1, 0),
(55505, 'Card Promotion', 12, 0, 1),
(55506, 'Inventory Clearance', 20, 1, 0),
(55507, 'Special VIP Discount', 7, 0, 1),
(55508, 'Anniversary Promotion', 18, 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_factura`
--

CREATE TABLE `detalle_factura` (
  `cantidad` int(11) NOT NULL,
  `cod_destalle` int(11) NOT NULL,
  `cod_factura` int(11) NOT NULL,
  `cod_producto` int(11) NOT NULL,
  `precio_unitario` double NOT NULL,
  `subtotal` double NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_factura`
--

INSERT INTO `detalle_factura` (`cantidad`, `cod_destalle`, `cod_factura`, `cod_producto`, `precio_unitario`, `subtotal`) VALUES
(2, 0, 10, 1, 45000, 90000);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empresas`
--

CREATE TABLE `empresas` (
  `cod_empresa` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `nit` varchar(255) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `ciudad` varchar(50) NOT NULL,
  `telefono` varchar(255) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empresas`
--

INSERT INTO `empresas` (`cod_empresa`, `nombre`, `nit`, `direccion`, `ciudad`, `telefono`, `correo`) VALUES
(1, 'Verdad y Reconciliacion', '980256314', 'Cll 28 # 9-47', 'Cali', '3206841435', 'verdadyreconciliacion@factugest.com'),
(2, 'Pillar of Autumn', '987654321', 'Av Caracas # 2-56', 'Cucuta', '3132156472', 'pillarofautumn@factugest.com'),
(6, 'Gran Caridad', '890345555', 'AV 10  # 3-21', 'Bogota', '312398888', 'grancaridad@factugest.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `facturas`
--

CREATE TABLE `facturas` (
  `cod_factura` int(11) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `cod_cliente` int(11) DEFAULT NULL,
  `cod_usuario` int(11) DEFAULT NULL,
  `cod_pago` int(11) DEFAULT NULL,
  `total` double NOT NULL,
  `cod_empresa` int(11) DEFAULT NULL,
  `cod_metodo_pago` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `facturas`
--

INSERT INTO `facturas` (`cod_factura`, `fecha`, `cod_cliente`, `cod_usuario`, `cod_pago`, `total`, `cod_empresa`, `cod_metodo_pago`) VALUES
(2, '2026-02-17 21:26:00.000000', 7, 1, 1, 1200000, 6, 1),
(3, '2026-02-19 09:33:40.000000', 6, 2, 3, 2500000, 2, 3),
(4, '2026-02-17 09:35:29.000000', 10, 3, 2, 1800000, 1, 2),
(5, '2026-02-06 09:36:21.000000', 8, 4, 4, 1700000, 6, 4),
(6, '2026-02-16 09:38:46.000000', 5, 5, 5, 150000, 2, 5),
(7, '2026-02-27 11:25:22.000000', 9, 2, 6, 1300000, 2, 3),
(8, '2026-02-25 11:26:02.000000', 3, 3, 7, 2500000, 1, 1),
(10, '2026-03-09 01:00:00.000000', 6, 1, 1, 90000, 1, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_descuento`
--

CREATE TABLE `factura_descuento` (
  `cod_descuento` int(11) NOT NULL,
  `cod_factura` int(11) NOT NULL,
  `valor_descuento` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `factura_impuesto`
--

CREATE TABLE `factura_impuesto` (
  `cod_factura` int(11) DEFAULT NULL,
  `cod_impuesto` int(11) DEFAULT NULL,
  `id_factura_impuesto` int(11) NOT NULL,
  `valor_impuesto` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `impuestos`
--

CREATE TABLE `impuestos` (
  `cod_impuesto` int(11) NOT NULL,
  `porcentaje` double NOT NULL,
  `descripcion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `impuestos`
--

INSERT INTO `impuestos` (`cod_impuesto`, `porcentaje`, `descripcion`) VALUES
(1, 19, 'IVA'),
(2, 2, 'RETEFUENTE'),
(3, 1, 'RETEICA'),
(6, 15, 'RETEIVA'),
(7, 0.8, 'RETECREE'),
(8, 0, 'EXENTO');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logs`
--

CREATE TABLE `logs` (
  `cod_usuario` int(11) NOT NULL,
  `id_log` int(11) NOT NULL,
  `fecha` datetime(6) NOT NULL,
  `accion` varchar(100) NOT NULL,
  `descripcion` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `logs`
--

INSERT INTO `logs` (`cod_usuario`, `id_log`, `fecha`, `accion`, `descripcion`) VALUES
(1, 1, '2026-03-01 08:00:15.000000', 'LOGIN', 'User logged in'),
(2, 2, '2026-03-01 08:10:32.000000', 'VIEW', 'Accessed the main dashboard'),
(1, 3, '2026-03-01 08:15:10.000000', 'CREATE', 'Created a new record'),
(3, 4, '2026-03-01 09:02:55.000000', 'LOGIN', 'Successful login'),
(2, 5, '2026-03-01 09:15:45.000000', 'UPDATE', 'Updated information');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `metodos_pago`
--

CREATE TABLE `metodos_pago` (
  `cod_pago` int(11) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `metodos_pago`
--

INSERT INTO `metodos_pago` (`cod_pago`, `descripcion`, `nombre`) VALUES
(1, 'CASH', NULL),
(2, 'DEBIT CARD', NULL),
(3, 'CREDIT CARD', NULL),
(4, 'BANK TRANSFER', NULL),
(5, 'Sistecuerpo', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos_factura`
--

CREATE TABLE `pagos_factura` (
  `status` varchar(20) NOT NULL,
  `cod_pago_factura` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos_factura`
--

INSERT INTO `pagos_factura` (`status`, `cod_pago_factura`) VALUES
('paid', 1),
('pending', 2),
('partially paid', 3),
('overdue', 4),
('cancelled', 5),
('disputed', 6),
('refunded', 7);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `cod_producto` int(11) NOT NULL,
  `sku` varchar(50) NOT NULL COMMENT 'Código interno único para el negocio',
  `nombre` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `precio_unitario` decimal(12,2) NOT NULL COMMENT 'Decimal para precisión monetaria',
  `stock` int(11) DEFAULT 0,
  `stock_minimo` int(11) DEFAULT 5 COMMENT 'Alerta para reabastecimiento',
  `cod_impuesto` int(11) NOT NULL DEFAULT 1 COMMENT 'FK a tabla impuestos. 1 = IVA 19% por defecto',
  `unidad_medida` varchar(20) DEFAULT '94' COMMENT 'Código estándar (ej. C62=Unidad, WSD=servicios, KGM=Kilogramo)',
  `codigo_barras` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`cod_producto`, `sku`, `nombre`, `descripcion`, `precio_unitario`, `stock`, `stock_minimo`, `cod_impuesto`, `unidad_medida`, `codigo_barras`, `activo`) VALUES
(1, 'TEC-001', 'Logitech Wireless Mouse', 'Ergonomic black mouse, AA battery included', 45000.00, 50, 10, 1, 'C62', NULL, 1),
(2, 'TEC-002', 'RGB Mechanical Keyboard', 'Gaming keyboard with blue switches, backlit', 180000.00, 20, 5, 1, 'C62', NULL, 1),
(3, 'TEC-003', 'Samsung 24\" Monitor', 'LED IPS 75Hz display, HDMI/VGA', 650000.00, 2, 3, 1, 'C62', NULL, 1),
(4, 'ACC-001', 'Laptop Backpack', 'Waterproof backpack for laptops up to 15.6\"', 95000.00, 30, 5, 1, 'C62', NULL, 1),
(5, 'SER-001', 'Preventive Maintenance', 'PC cleaning and optimization technical service', 80000.00, 999, 0, 1, 'WSD', NULL, 1),
(6, 'TEC-004', '480GB SSD Solid State Drive', 'Kingston SATA III solid state drive', 120000.00, 40, 8, 1, 'C62', NULL, 1),
(7, 'TEC-005', '2 Meter HDMI Cable', 'Reinforced 4K high-speed cable', 15000.00, 15, 20, 1, 'C62', NULL, 1),
(8, 'LIC-001', '1 Year Antivirus License', 'Digital activation code sent via email', 55000.00, 999, 0, 1, 'WSD', NULL, 1),
(9, 'TEC-006', '8GB DDR4 RAM Memory', 'Laptop memory module 2666MHz', 110000.00, 25, 5, 1, 'C62', NULL, 1),
(10, 'PAP-001', 'Letter Size Bond Paper Ream', 'White paper box 75g x 500 sheets', 18500.00, 0, 0, 1, 'C62', NULL, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos_descuentos`
--

CREATE TABLE `productos_descuentos` (
  `cod_descuento` int(11) NOT NULL,
  `cod_producto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos_descuentos`
--

INSERT INTO `productos_descuentos` (`cod_descuento`, `cod_producto`) VALUES
(15, 3),
(20, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto_descuento`
--

CREATE TABLE `producto_descuento` (
  `cod_producto` int(11) NOT NULL,
  `cod_descuento` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto_descuento`
--

INSERT INTO `producto_descuento` (`cod_producto`, `cod_descuento`) VALUES
(1, 55504),
(2, 55506),
(3, 55501),
(6, 55508);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `cod_usuario` int(11) NOT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `correo` varchar(255) DEFAULT NULL,
  `contrasena` varchar(255) DEFAULT NULL,
  `rol` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`cod_usuario`, `nombre`, `correo`, `contrasena`, `rol`) VALUES
(1, 'Administrator', 'administrador@factugest.com', '123456789', 'ADMIN'),
(2, 'Brandon', 'brandon@factugest.com', '123456789', 'ADMIN'),
(3, 'Johan', 'johan@factugest.com', '123456789', 'ADMIN'),
(4, 'Wilmer', 'wilmer@factugest.com', '123456789', 'ADMIN'),
(5, 'Yuliana', 'yuliana@factugest.com', '123456789', 'CAJERO');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`cod_cliente`),
  ADD UNIQUE KEY `numero_documento` (`numero_documento`);

--
-- Indices de la tabla `configuracion`
--
ALTER TABLE `configuracion`
  ADD PRIMARY KEY (`clave`);

--
-- Indices de la tabla `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD UNIQUE KEY `document_number` (`document_number`);

--
-- Indices de la tabla `descuentos`
--
ALTER TABLE `descuentos`
  ADD PRIMARY KEY (`cod_descuento`);

--
-- Indices de la tabla `detalle_factura`
--
ALTER TABLE `detalle_factura`
  ADD PRIMARY KEY (`cod_destalle`);

--
-- Indices de la tabla `empresas`
--
ALTER TABLE `empresas`
  ADD PRIMARY KEY (`cod_empresa`),
  ADD UNIQUE KEY `nit` (`nit`);

--
-- Indices de la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD PRIMARY KEY (`cod_factura`),
  ADD KEY `cod_usuario` (`cod_usuario`),
  ADD KEY `cod_empresa` (`cod_empresa`),
  ADD KEY `cod_pago` (`cod_pago`),
  ADD KEY `FKcxx7trc0b0xhuawwapbr4ogco` (`cod_metodo_pago`),
  ADD KEY `facturas_ibfk_1` (`cod_cliente`);

--
-- Indices de la tabla `factura_descuento`
--
ALTER TABLE `factura_descuento`
  ADD PRIMARY KEY (`cod_descuento`,`cod_factura`),
  ADD KEY `FKn9t3efsp0sk3egm9386gv9v7f` (`cod_factura`);

--
-- Indices de la tabla `factura_impuesto`
--
ALTER TABLE `factura_impuesto`
  ADD PRIMARY KEY (`id_factura_impuesto`),
  ADD KEY `FKa6ckq6lco6pjwp46oyx29v620` (`cod_factura`),
  ADD KEY `FKb3kag5880t417tnrsbop0mrrd` (`cod_impuesto`);

--
-- Indices de la tabla `impuestos`
--
ALTER TABLE `impuestos`
  ADD PRIMARY KEY (`cod_impuesto`);

--
-- Indices de la tabla `logs`
--
ALTER TABLE `logs`
  ADD PRIMARY KEY (`id_log`),
  ADD KEY `FKedv0n646ie560v5r7nqtbs9d5` (`cod_usuario`);

--
-- Indices de la tabla `metodos_pago`
--
ALTER TABLE `metodos_pago`
  ADD PRIMARY KEY (`cod_pago`);

--
-- Indices de la tabla `pagos_factura`
--
ALTER TABLE `pagos_factura`
  ADD PRIMARY KEY (`cod_pago_factura`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`cod_producto`),
  ADD UNIQUE KEY `sku` (`sku`),
  ADD KEY `fk_producto_impuesto` (`cod_impuesto`);

--
-- Indices de la tabla `productos_descuentos`
--
ALTER TABLE `productos_descuentos`
  ADD PRIMARY KEY (`cod_descuento`);

--
-- Indices de la tabla `producto_descuento`
--
ALTER TABLE `producto_descuento`
  ADD PRIMARY KEY (`cod_producto`,`cod_descuento`),
  ADD KEY `cod_descuento` (`cod_descuento`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`cod_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `cod_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `descuentos`
--
ALTER TABLE `descuentos`
  MODIFY `cod_descuento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=665659;

--
-- AUTO_INCREMENT de la tabla `empresas`
--
ALTER TABLE `empresas`
  MODIFY `cod_empresa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `facturas`
--
ALTER TABLE `facturas`
  MODIFY `cod_factura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `factura_impuesto`
--
ALTER TABLE `factura_impuesto`
  MODIFY `id_factura_impuesto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `impuestos`
--
ALTER TABLE `impuestos`
  MODIFY `cod_impuesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `logs`
--
ALTER TABLE `logs`
  MODIFY `id_log` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `metodos_pago`
--
ALTER TABLE `metodos_pago`
  MODIFY `cod_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `pagos_factura`
--
ALTER TABLE `pagos_factura`
  MODIFY `cod_pago_factura` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `cod_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `productos_descuentos`
--
ALTER TABLE `productos_descuentos`
  MODIFY `cod_descuento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `cod_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `facturas`
--
ALTER TABLE `facturas`
  ADD CONSTRAINT `FKcxx7trc0b0xhuawwapbr4ogco` FOREIGN KEY (`cod_metodo_pago`) REFERENCES `metodos_pago` (`cod_pago`),
  ADD CONSTRAINT `facturas_ibfk_1` FOREIGN KEY (`cod_cliente`) REFERENCES `customers` (`customer_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `facturas_ibfk_2` FOREIGN KEY (`cod_usuario`) REFERENCES `usuarios` (`cod_usuario`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `facturas_ibfk_3` FOREIGN KEY (`cod_empresa`) REFERENCES `empresas` (`cod_empresa`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `facturas_ibfk_4` FOREIGN KEY (`cod_pago`) REFERENCES `pagos_factura` (`cod_pago_factura`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `factura_descuento`
--
ALTER TABLE `factura_descuento`
  ADD CONSTRAINT `FKn9t3efsp0sk3egm9386gv9v7f` FOREIGN KEY (`cod_factura`) REFERENCES `facturas` (`cod_factura`),
  ADD CONSTRAINT `FKqum49fhp3hw13koeag0pcf564` FOREIGN KEY (`cod_descuento`) REFERENCES `descuentos` (`cod_descuento`);

--
-- Filtros para la tabla `factura_impuesto`
--
ALTER TABLE `factura_impuesto`
  ADD CONSTRAINT `FKa6ckq6lco6pjwp46oyx29v620` FOREIGN KEY (`cod_factura`) REFERENCES `facturas` (`cod_factura`),
  ADD CONSTRAINT `FKb3kag5880t417tnrsbop0mrrd` FOREIGN KEY (`cod_impuesto`) REFERENCES `impuestos` (`cod_impuesto`);

--
-- Filtros para la tabla `logs`
--
ALTER TABLE `logs`
  ADD CONSTRAINT `FKedv0n646ie560v5r7nqtbs9d5` FOREIGN KEY (`cod_usuario`) REFERENCES `usuarios` (`cod_usuario`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `fk_producto_impuesto` FOREIGN KEY (`cod_impuesto`) REFERENCES `impuestos` (`cod_impuesto`);

--
-- Filtros para la tabla `producto_descuento`
--
ALTER TABLE `producto_descuento`
  ADD CONSTRAINT `producto_descuento_ibfk_2` FOREIGN KEY (`cod_descuento`) REFERENCES `descuentos` (`cod_descuento`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
