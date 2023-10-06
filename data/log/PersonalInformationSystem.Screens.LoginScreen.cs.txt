using PersonalInformationSystem.TemplateScreens;
using System;
using System.Windows.Forms;

namespace PersonalInformationSystem.Screens
{
    public partial class LoginScreen : BaseTemplateScreen
    {
        public LoginScreen()
        {
            InitializeComponent();
        }

        private void ExitButton_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void ShowPasswordCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            if (PasswordTextBox.UseSystemPasswordChar == true)
                PasswordTextBox.UseSystemPasswordChar = false;
            else
                PasswordTextBox.UseSystemPasswordChar = true;
        }

        private void LoginButton_Click(object sender, EventArgs e)
        {
            if(IsDataValid())
            {
                // Database Login
            } 
        }

        private bool IsDataValid()
        {
            // Validation (Data Entry Validation)
            if (UserNameTextBox.Text == string.Empty)
            {
                MessageBox.Show("User Name is required.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                UserNameTextBox.Focus();

                return false;
            }


            if (PasswordTextBox.Text == string.Empty)
            {
                MessageBox.Show("Password is required.", "Validation Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                PasswordTextBox.Focus();

                return false;
            }

            return true;
        }
    }
}
