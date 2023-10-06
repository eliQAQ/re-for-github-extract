package db_connec_test;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.*;
import java.awt.*;
import java.awt.event.*;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.swing.*;

@SuppressWarnings("serial")
public class Intro extends JFrame {
	JMenuBar menubar;
	JMenu help;
	JMenuItem info;
	JComponent buttonPane;
	private static String OK = "ok";
	private static String REGISTER = "register";
	private JFrame controllingFrame; // needed for dialogs
	private JTextField idField;
	private JPasswordField passwordField;
	public static Connection con;
	public static PreparedStatement st;
	public static ResultSet rs;

	public static String correct_id;
	public static int no_id;

	public Intro() {

		pwEvent f = new pwEvent();

		setLayout(new FlowLayout());
		menubar = new JMenuBar();
		add(menubar);
		help = new JMenu("Help");
		menubar.add(help);
		info = new JMenuItem("IPMS Ver.1.0");
		help.add(info);
		setJMenuBar(menubar);
		event e = new event();
		info.addActionListener(e);

		idField = new JTextField(10);
		passwordField = new JPasswordField(10);
		passwordField.addActionListener(f);

		JLabel label1 = new JLabel("id: ");
		label1.setLabelFor(idField);

		JLabel label = new JLabel("password: ");
		label.setLabelFor(passwordField);

		JPanel textPane = new JPanel();
		textPane.setLayout(new GridLayout(2, 1));

		textPane.add(label1);
		textPane.add(idField);

		textPane.add(label);
		textPane.add(passwordField);

		add(textPane);
		JPanel p = new JPanel(new GridLayout(0, 1));
		JButton okButton = new JButton("OK");
		JButton registerButton = new JButton("REGISTER");

		okButton.setActionCommand(OK);
		registerButton.setActionCommand(REGISTER);

		okButton.addActionListener(f);
		registerButton.addActionListener(f);

		p.add(okButton);
		p.add(registerButton);

		add(p);
	}

	public class event implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			Info gui = new Info(Intro.this);
			gui.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
			gui.setSize(300, 100);
			gui.setLocation(300, 500);
			gui.setVisible(true);

		}
	}

	// checks both ID and password
	public class pwEvent implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			String cmd = e.getActionCommand();

			if (REGISTER.equals(cmd)) {
				try {
					new registerForm();
				} catch (SQLException e2) {
					// TODO Auto-generated catch block
					e2.printStackTrace();
				}
			} else {
				@SuppressWarnings("deprecation")
				String input = passwordField.getText();
				String id_input = idField.getText();
				if (id_input.length() == 0) {
					JOptionPane.showMessageDialog(controllingFrame, "Please enter your ID!", "Error Message",
							JOptionPane.ERROR_MESSAGE);
					return;
				} else if (input.length() == 0) {
					JOptionPane.showMessageDialog(controllingFrame, "Please enter your password", "Error Message",
							JOptionPane.ERROR_MESSAGE);
					return;
				}
				try {
					if (isIDCorrect(id_input, input)) {
						new decryptForm(no_id);
						dispose();
					} else {
						JOptionPane.showMessageDialog(controllingFrame, "Invalid ID or Password!! Try again!",
								"Error Message", JOptionPane.ERROR_MESSAGE);
					}
				} catch (HeadlessException | SQLException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

				// Zero out the possible password, for security.
				input = null;
				passwordField.selectAll();
				resetFocus();
			}
		}
	}

	private static boolean isIDCorrect(String input, String input_pw) throws SQLException {
		boolean isCorrect = true;

		con = DriverManager.getConnection("jdbc:mysql://127.0.0.1/mof?useUnicode=true&characterEncoding=euckr", "root",
				"1234");
		st = con.prepareStatement("SELECT * FROM `account` WHERE `id`=? AND `pw`=?");
		String hashed_pw = SHA256(input_pw + input);
		st.setString(1, input);
		st.setString(2, hashed_pw);

		rs = st.executeQuery();

		if (rs.next()) {
			no_id = rs.getInt("no");
		} else {
			isCorrect = false;
		}
		
		return isCorrect;
	}

	protected void resetFocus() {
		passwordField.requestFocusInWindow();
	}

	public static void main(String args[]) {
		Intro gui = new Intro();
		gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		gui.setSize(500, 300);
		gui.setLocationRelativeTo(null);

		gui.setVisible(true);
		gui.setResizable(false);

		gui.setTitle("IMPS Ver.1.0");
	}

	public static String SHA256(String str) {

		String encryption = "";

		try {
			MessageDigest hash = MessageDigest.getInstance("SHA-256");
			hash.update(str.getBytes());
			byte byteData[] = hash.digest();
			StringBuffer sb = new StringBuffer();

			for (int i = 0; i < byteData.length; i++) {
				sb.append(Integer.toString((byteData[i] & 0xff) + 0x100, 16).substring(1));
			}
			encryption = sb.toString();
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
			encryption = null;
		}

		return encryption;
	}
}
