USE [account_socket]
GO
/****** Object:  Table [dbo].[User_account]    Script Date: 29/10/2021 2:15:19 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[User_account](
	[username] [nchar](10) NOT NULL,
	[password] [nchar](10) NOT NULL
) ON [PRIMARY]
GO
INSERT [dbo].[User_account] ([username], [password]) VALUES (N'tvh       ', N'123a      ')
INSERT [dbo].[User_account] ([username], [password]) VALUES (N'vmh       ', N'123456    ')
INSERT [dbo].[User_account] ([username], [password]) VALUES (N'tada      ', N'123       ')
GO
