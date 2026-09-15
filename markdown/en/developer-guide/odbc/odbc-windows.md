# Installing and configuring the ODBC Driver for Windows

Windows utilizes named data sources (DSNs) for connecting ODBC-based client applications to Snowflake.

## Prerequisites

### Operating system

For a list of the operating systems supported by Snowflake clients, see [Operating system support](/release-notes/requirements#label-client-operating-system-support).

### Administrator privileges

To install the ODBC driver, you need administrator-level privileges so
that the driver can be installed in the `C:Program Files` directory.

### Visual C++ Redistributable for Visual Studio 2015

To use Snowflake ODBC Driver in a Windows environment, you have to first install Visual C++ Redistributable for Visual Studio 2015.

You can download the installation file from:

> <https://learn.microsoft.com/en-us/cpp/windows/latest-supported-vc-redist?view=msvc-170#visual-studio-2015-2017-2019-and-2022>

## Step 1: Install the ODBC Driver

1. If you haven’t already downloaded the latest driver version, download it now. For details, see [Downloading the ODBC Driver](/developer-guide/odbc/odbc-download).
2. Double-click on the downloaded .msi file:

   Note

   The driver is installed in `C:Program Files`.

## Step 2: Configure the ODBC Driver

To configure the ODBC driver in a Windows environment, create a DSN for the driver:

1. Launch the Windows Data Source Administration Tool:

   Search on your Windows machine for the launcher for the ODBC Data Source Administration Tool:

   ![Configuring ODBC for Windows](/static/images/screens/odbc1.png)

   Once you find the ODBC administration tool, click on the tool to launch it and display the set up window.
2. Verify that the Snowflake ODBC driver is installed:

   Navigate to the **Drivers** tab in the set up window and verify that the driver (SnowflakeDSIIDriver) appears:

   ![Configuring ODBC for Windows](/static/images/screens/odbc2.png)

   If you do not see **SnowflakeDSIIDriver**, then the Snowflake ODBC driver installation did not complete successfully and you need to re-install it.
3. Create a new DSN:

   1. Navigate to the **User DSN** or **System DSN** tab and click the **Add** button:

      ![Configuring ODBC for Windows](/static/images/screens/odbc3.png)
   2. Select **SnowflakeDSIIDriver** from the list of installed drivers.
   3. Enter the connection parameters for the driver.

      In the fields provided in **Snowflake Configuration** dialog, enter the parameters for the DSN:

      ![Configuring ODBC for Windows](/static/images/screens/odbc4.png)

      When entering parameters, note the following:

      - **Data Source**, **User** and **Server** are the only parameters required to create a DSN.

        For more information on these parameters, see [Required connection parameters](/developer-guide/odbc/odbc-parameters#label-odbc-connection-parameters-required).
      - All other parameters in the dialog are optional. In particular, the
        proxy-related parameters should be specified only if you are using a proxy, and the
        Authenticator should be changed from the default (“snowflake”) only if needed.
        For more details about ODBC Data Source parameters, see
        [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters)
        and, in particular, [Optional connection parameters](/developer-guide/odbc/odbc-parameters#label-odbc-optional-connection-parameters).
      - The **Password** field accepts a value, but does not store the value. This is a security precaution to ensure passwords are never stored directly in the driver.

      Note

      - The ODBC driver supports additional parameters that are not displayed in the dialog. These parameters can only be set in the Windows registry using **regedit**.

        For descriptions of all the parameters, see [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters).
      - Specifying a value in the **Authenticator** field is only required if you are using federated authentication. For more information, see the `authenticator` parameter description in [ODBC configuration and connection parameters](/developer-guide/odbc/odbc-parameters).
   4. Click **OK** to create the DSN.

You can now reference this DSN in ODBC-based client applications for connecting to Snowflake.
