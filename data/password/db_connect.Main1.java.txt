package db_connec_test;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.awt.event.WindowEvent;
import java.awt.event.WindowListener;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.UnsupportedEncodingException;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;



//library for email
import java.util.Properties;
import java.util.Random;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.NoSuchProviderException;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

@SuppressWarnings("serial")
public class Main1 extends Intro implements MouseListener, ActionListener, WindowListener {
	JFrame jp = new JFrame("IPMS");
	JTable jt;
	@SuppressWarnings("rawtypes")
	JComboBox box;
	DefaultTableModel dtm;
	InputForm form;
	DeactivateForm form_deactivate;
	SearchForm form_search;
	EditMasterForm form_master;
	EditEmailForm form_email;
	int srow;
	JMenuBar menuBar = new JMenuBar();
	JMenu mainMenu = new JMenu("Menu");
	JMenu helpMenu = new JMenu("Help");
	JMenuItem Deactivate = new JMenuItem("Account Setting");
	JMenuItem editMaster = new JMenuItem("Edit master password");
	JMenuItem editEmail = new JMenuItem("Edit master email");
	JMenuItem logOut = new JMenuItem("Log Out");
	JMenuItem exit = new JMenuItem("Exit");
	JMenuItem version = new JMenuItem("Version");
	JMenuItem info = new JMenuItem("Info");
	JScrollPane scroll;
	JLabel label, label_info;
	JPanel northp, southp;
	JButton bt_add, bt_del, bt_up, bt_search;

	Object[][] rowData = {};

	Object[] columnNames = { "Name", "ID", "Password", "link" };

	// connecting database
	public static Connection con;
	public static Statement st;
	public static ResultSet rs;
	public static Statement st2;
	public static ResultSet rs2;

	public static String name_edit;
	public static String url_edit;
	public static String id_edit;
	public static String pw_edit;

	public static int id_num;

	public static String key;

	public Main1(int no_id, String get_key) throws SQLException {

		id_num = no_id;

		try {
			con = DriverManager.getConnection("jdbc:mysql://127.0.0.1/mof?useUnicode=true&characterEncoding=euckr",
					"root", "1234");
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		try {
			st = con.createStatement();
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}

		st2 = con.createStatement();

		dtm = new DefaultTableModel(rowData, columnNames);

		String sql = "select * from `keys` where `acnt_no` = " + no_id + "";
		rs = st.executeQuery(sql);

		if (st.execute(sql)) {
			rs = st.getResultSet();
		}

		while (rs.next()) {
			String str = rs.getString("title");
			String name = str;

			str = rs.getString("url");
			String link = str;

			str = rs.getString("id_sequence");
			String id = str;

			str = rs.getString("pw_sequence");
			String pw = str;

			Encryptor aes256 = null;
			try {
				aes256 = new Encryptor(get_key);
			} catch (UnsupportedEncodingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			String decText = null;
			try {
				decText = aes256.aesDecode(pw);
			} catch (InvalidKeyException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (UnsupportedEncodingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (NoSuchAlgorithmException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (NoSuchPaddingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (InvalidAlgorithmParameterException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IllegalBlockSizeException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (BadPaddingException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

			Object rowData[] = { name, id, decText, link };
			dtm.addRow(rowData);
		}

		form = new InputForm();
		form_search = new SearchForm();
		form_deactivate = new DeactivateForm();
		form_email = new EditEmailForm();
		form_master = new EditMasterForm();
		box = form_search.box;

		jt = new JTable(dtm);
		scroll = new JScrollPane(jt);
		label = new JLabel("IPMS");
		northp = new JPanel();
		northp.add(label);

		bt_add = new JButton("Add new");
		bt_del = new JButton("Delete");
		bt_up = new JButton("Edit");
		bt_search = new JButton("Search");

		southp = new JPanel();
		southp.add(bt_add);
		southp.add(bt_del);
		southp.add(bt_up);
		southp.add(bt_search);

		jp.add("Center", scroll);
		jp.add("North", northp);
		jp.add("South", southp);
		jp.setBounds(400, 300, 300, 300);
		jp.setSize(1000, 700);
		jp.setVisible(true);
		jp.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

		eventUp();

		// create menu
		mainMenu.add(Deactivate);
		mainMenu.add(editEmail);
		mainMenu.add(editMaster);
		mainMenu.addSeparator(); // separator

		mainMenu.add(logOut);
		mainMenu.addSeparator();
		mainMenu.add(exit);
		helpMenu.add(info);

		// add menu to menubar
		menuBar.add(mainMenu);
		menuBar.add(helpMenu);

		// add menubar
		jp.setJMenuBar(menuBar);

		jp.setLocationRelativeTo(null);
		jp.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
	}

	private void eventUp() {
		jt.addMouseListener(this);

		mainMenu.addActionListener(this);
		helpMenu.addActionListener(this);
		bt_add.addActionListener(this);
		bt_del.addActionListener(this);
		bt_up.addActionListener(this);
		bt_search.addActionListener(this);

		form_deactivate.bt_input.addActionListener(this);
		form_deactivate.bt_cancel.addActionListener(this);

		form.bt_input.addActionListener(this);
		form.bt_cancel.addActionListener(this);

		form_search.bt_input.addActionListener(this);
		form_search.bt_cancel.addActionListener(this);

		form_email.bt_input.addActionListener(this);
		form_email.bt_cancel.addActionListener(this);

		form_master.bt_input.addActionListener(this);
		form_master.bt_cancel.addActionListener(this);

		Deactivate.addActionListener(this);
		editEmail.addActionListener(this);
		editMaster.addActionListener(this);
		logOut.addActionListener(this);
		exit.addActionListener(this);
		info.addActionListener(this);
	}

	public void actionPerformed(ActionEvent e) {

		try {
			con = DriverManager.getConnection("jdbc:mysql://127.0.0.1/mof?useUnicode=true&characterEncoding=euckr",
					"root", "1234");
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}
		try {
			st = con.createStatement();
		} catch (SQLException e2) {
			// TODO Auto-generated catch block
			e2.printStackTrace();
		}

		Object ob = e.getSource();
		if (ob == bt_add) { // add button
			form.initTF();
			form.setVisible(true);
		} else if (ob == form.bt_input) { // input button (insert / edit)

			String name = form.tf_name.getText();
			String id = form.tf_id.getText();
			String pw = form.tf_pw.getText();
			String link = form.tf_link.getText();

			if (name == null || name.length() == 0) {
				// check nullable
				JOptionPane.showMessageDialog(form, "Input name!!");
				form.tf_name.requestFocus();
				return;
			}

			if (id.length() == 0) {
				JOptionPane.showMessageDialog(form, "Input ID!!");
				form.tf_id.requestFocus();
				return;
			}

			if (pw.length() == 0) {
				JOptionPane.showMessageDialog(form, "Input password!!");
				form.tf_pw.requestFocus();
				return;
			}

			if (link.length() == 0) {
				JOptionPane.showMessageDialog(form, "Input link!!");
				form.tf_link.requestFocus();
				return;
			}

			String query_name = "'" + name + "'";
			String query_id = "'" + id + "'";
			String query_pw = "'" + pw + "'";
			String query_link = "'" + link + "'";

			if (form.strength.getValue() < 20) {
				JOptionPane.showMessageDialog(form, "Password is too weak!");
				form.tf_pw.requestFocus();
				return;
			}

			if (form.getTitle().equals("Add new")) { // add new form

				String sql = "INSERT INTO `keys` (`acnt_no`, `title`, `url`, `id_sequence`, `pw_sequence`) VALUES ("
						+ id_num + "," + query_name + "," + query_link + "," + query_id + "," + query_pw + ")";

				try {
					st.executeUpdate(sql);
				} catch (SQLException e2) {
					// TODO Auto-generated catch block
					e2.printStackTrace();
				}

				Object rowData[] = { name, id, pw, link };
				dtm.addRow(rowData);
				try {
					fileSave();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

			} else { // edit form

				jt.setValueAt(name, srow, 0); // edit name
				jt.setValueAt(id, srow, 1); // edit id
				jt.setValueAt(pw, srow, 2); // edit pw
				jt.setValueAt(link, srow, 3); // edit link
				try {
					fileSave();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

				String sql = "UPDATE `keys` SET `title` = " + query_name + ", `url` = " + query_link
						+ ", `id_sequence` = " + query_id + ", `pw_sequence` = " + query_pw + " WHERE `acnt_no` = "
						+ id_num + " and `title` = '" + name_edit + "' and `pw_sequence` = '" + pw_edit
						+ "' and `url` = '" + url_edit + "'";
				try {
					st.executeUpdate(sql);
				} catch (SQLException e2) {
					// TODO Auto-generated catch block
					e2.printStackTrace();
				}

			}
			form.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == form.bt_cancel) { // cancel button
			form.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == bt_del) { // delete button
			srow = jt.getSelectedRow();
			if (srow == -1) {
				JOptionPane.showMessageDialog(jp, "Select row to delete!!");
				return;
			}
			String name = (String) jt.getValueAt(srow, 0);
			name_edit = name;
			String id = (String) jt.getValueAt(srow, 1);
			id_edit = id;
			String pw = (String) jt.getValueAt(srow, 2);
			pw_edit = pw;
			String link = (String) jt.getValueAt(srow, 3);
			url_edit = link;

			String sql = "DELETE FROM `keys` WHERE `acnt_no` = " + id_num + " and `title` = '" + name_edit
					+ "' and `pw_sequence` = '" + pw_edit + "' and `url` = '" + url_edit + "'";
			try {
				st.executeUpdate(sql);
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			for (int i = 0; i < jt.getRowCount(); i++) {
				if (name.equals(jt.getValueAt(i, 0)) && id.equals(jt.getValueAt(i, 1)) && pw.equals(jt.getValueAt(i, 2))
						&& link.equals(jt.getValueAt(i, 3))) {
					dtm.removeRow(i);
				}
			}
			try {
				fileSave();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		} else if (ob == bt_up) { // edit button
			srow = jt.getSelectedRow();

			if (srow == -1) { // if unselected, srow value is -1
				JOptionPane.showMessageDialog(jp, "Select row to edit!!");
				return;
			}

			String name = (String) jt.getValueAt(srow, 0);
			name_edit = name;
			String id = (String) jt.getValueAt(srow, 1);
			id_edit = id;
			String pw = (String) jt.getValueAt(srow, 2);
			pw_edit = pw;
			String link = (String) jt.getValueAt(srow, 3);
			url_edit = link;

			form.tf_name.setText(name);
			form.tf_id.setText(id);
			form.tf_pw.setText(pw);
			form.tf_link.setText(link);
			form.initUp();
			form.setVisible(true);
		} else if (ob == bt_search) { // search button

			String tf = form_search.tf.getText();

			form_search.tf.setText(tf);
			form_search.initSearch();
			form_search.setVisible(true);
		} else if (ob == form_search.bt_input) {
			String input = form_search.tf.getText();

			if (input == null || input.length() == 0) {
				// check nullable
				JOptionPane.showMessageDialog(form, "Input anything please!!");
				form_search.tf.requestFocus();
				return;
			} else {
				if (box.getSelectedItem() == "Name") {
					for (int i = 0; i < rowData.length; i++) {
						if (input.compareTo((String) rowData[i][0]) == 0) {
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(false);
					jp.setVisible(true);
				} else if (box.getSelectedItem() == "ID") {
					for (int i = 0; i < rowData.length; i++) {
						if (input.compareTo((String) rowData[i][1]) == 0) {
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(true);
					jp.setVisible(true);
				} else if (box.getSelectedItem() == "Password") {
					for (int i = 0; i < rowData.length; i++) {
						if (input.compareTo((String) rowData[i][2]) == 0) {
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(false);
					jp.setVisible(true);
				} else {
					for (int i = 0; i < rowData.length; i++) {
						if (input.compareTo((String) rowData[i][3]) == 0 || ((String) rowData[i][3]).contains(input)) {
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(false);
					jp.setVisible(true);
				}
			}

		} else if (ob == form_search.bt_cancel) {
			form_search.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == Deactivate) {
			form_deactivate.initDeactivate();
			form_deactivate.setVisible(true);
		} else if (ob == form_deactivate.bt_input) {
			String sql2 = "SELECT * FROM `account` WHERE `no` = " + no_id + "";
			String current_pw = form_deactivate.tf_pw.getText();
			String confirm_pw = form_deactivate.tf_confirm.getText();
			String check_pw = null;
			String ori_pw = null;
			String salt = null;

			try {
				rs = st.executeQuery(sql2);
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			try {
				while (rs.next()) {
					ori_pw = rs.getString("pw");
					salt = rs.getString("id");
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			check_pw = hash256(current_pw + salt);

			if (current_pw == null || current_pw.length() == 0) {
				JOptionPane.showMessageDialog(form_deactivate, "Input Your Password!!");
				form_deactivate.tf_pw.requestFocus();
				return;
			}

			if (confirm_pw == null || confirm_pw.length() == 0) {
				JOptionPane.showMessageDialog(form_deactivate, "Confirm Your Password!!");
				form_deactivate.tf_confirm.requestFocus();
				return;
			}

			if (current_pw.equals(confirm_pw) == false) {
				JOptionPane.showMessageDialog(form_deactivate, "Password not Confirmed properly! Try Again!!");
				form_deactivate.tf_confirm.requestFocus();
				return;
			}

			if (ori_pw.equals(check_pw) == false) {
				JOptionPane.showMessageDialog(form_deactivate, "Incorrect Password");
				form_deactivate.tf_pw.requestFocus();
				return;
			}

			String delete = "DELETE FROM `keys` WHERE `acnt_no` = " + id_num + "";

			try {
				st.executeUpdate(delete);
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			String sql = "DELETE FROM `account` WHERE `no` = " + id_num + "";

			try {
				st.executeUpdate(sql);
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			form_deactivate.setVisible(false);
			jp.setVisible(false);

			Intro gui = new Intro();
			gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			gui.setSize(500, 300);
			gui.setLocationRelativeTo(null);
			gui.setVisible(true);
			gui.setResizable(false);

			gui.setTitle("IMPS Ver.1.0");
		} else if (ob == form_deactivate.bt_cancel) {
			form_deactivate.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == editEmail) {
			form_email.initEditEmail();
			form_email.setVisible(true);
		} else if (ob == form_email.bt_input) {
			String email = form_email.tf_email.getText();

			if (email == null || email.length() == 0) {
				JOptionPane.showMessageDialog(form_email, "Input New Email!!");
				form_email.tf_email.requestFocus();
				return;
			}

			String sql = "UPDATE `account` SET `email` = '" + email + "' WHERE `no` = " + id_num + "";
			try {
				st.executeUpdate(sql);
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			form_email.setVisible(false);
			jp.setVisible(true);
		} else if (ob == form_email.bt_cancel) {
			form_email.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == editMaster) {
			form_master.initEditMaster();
			form_master.setVisible(true);
		} else if (ob == form_master.bt_input) {
			String current = form_master.tf_current.getText();
			String pw = form_master.tf_pw.getText();
			String confirm = form_master.tf_confirm.getText();
			String check = null;
			String salt = null;

			String sql2 = "SELECT * from `account` where `no` = " + id_num + "";

			try {
				rs = st.executeQuery(sql2);
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			try {
				if (st.execute(sql2)) {
					rs = st.getResultSet();
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			try {
				while (rs.next()) {
					check = rs.getString("pw");
					salt = rs.getString("id");
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			// check null - if there is no input in any of the fields, do not
			// accept

			current = hash256(current + salt);

			if (!check.equals(current)) {
				JOptionPane.showMessageDialog(form_master, "Current Password is wrong!!");
				form_master.tf_pw.requestFocus();
				return;
			}

			if (current == null || current.length() == 0) {
				JOptionPane.showMessageDialog(form_master, "Input Current Password!!");
				form_master.tf_pw.requestFocus();
				return;
			}

			if (pw == null || pw.length() == 0) {
				JOptionPane.showMessageDialog(form_master, "Input New Password!!");
				form_master.tf_pw.requestFocus();
				return;
			}

			if (confirm.length() == 0) {
				JOptionPane.showMessageDialog(form_master, "Confirm New Password!!");
				form_master.tf_confirm.requestFocus();
				return;
			}

			if (confirm.equals(pw) == false) {
				JOptionPane.showMessageDialog(form_master, "Password not Confirmed properly! Try Again!!");
				form_master.tf_confirm.requestFocus();
				return;
			}

			pw = hash256(pw + salt);

			String sql = "UPDATE `account` SET `pw` = '" + pw + "' WHERE `no` = " + id_num + "";
			try {
				st.executeUpdate(sql);
			} catch (SQLException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			form_master.setVisible(false);
			jp.setVisible(true);
		} else if (ob == form_master.bt_cancel) {
			form_master.setVisible(false);
			jp.setVisible(true);
		}

		else if (ob == logOut) {
			String pw_query = "select * from `keys` where `acnt_no` = " + id_num + "";

			StringBuffer keyBuff = new StringBuffer();
			key = new String();
			String keySource = new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*?/");
			while (keyBuff.length() < 16) {
				Random r = new Random();
				int index = r.nextInt(keySource.length());
				keyBuff.append(keySource.charAt(index));
			}
			key = keyBuff.toString();

			Encryptor aes256 = null;
			try {
				aes256 = new Encryptor(key);
			} catch (UnsupportedEncodingException e4) {
				// TODO Auto-generated catch block
				e4.printStackTrace();
			}

			try {
				rs = st.executeQuery(pw_query);
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}

			try {
				if (st.execute(pw_query)) {
					rs = st.getResultSet();
				}
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}

			try {
				while (rs.next()) {
					String user_pw = rs.getString("pw_sequence");
					String text = new String(user_pw);
					String encText = null;
					try {
						encText = aes256.aesEncode(text);
					} catch (InvalidKeyException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (UnsupportedEncodingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (NoSuchAlgorithmException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (NoSuchPaddingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (InvalidAlgorithmParameterException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (IllegalBlockSizeException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (BadPaddingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					String update_query = "UPDATE `keys` SET `pw_sequence` = '" + encText + "' WHERE `acnt_no` = "
							+ id_num + " and `pw_sequence` = '" + user_pw + "'";

					st2.executeUpdate(update_query);
				}
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}

			String sql2 = "select * from `account` where `no` = " + id_num + "";

			try {
				rs = st.executeQuery(sql2);
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			try {
				if (st.execute(sql2)) {
					rs = st.getResultSet();
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			String str = null;
			String user_name = null;

			try {
				while (rs.next()) {
					str = rs.getString("email");
					user_name = rs.getString("name");
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			// Mail configuration
			String host = "smtp.gmail.com";
			String username = "ku.mofteam@gmail.com";
			String password = "1q2w3e@@";

			// Set mail contents
			String recipient = "" + str + "";
			String subject = "Thanks for using our IPMS.";
			String body = "Dear " + user_name + "\n" + "Thanks for using our IPMS service.\n"
					+ "Your decryption key is " + key + "\n" + "Many thanks for your time";

			// Set properties
			Properties props = new Properties();
			props.put("mail.smtps.auth", "true");

			// Mail session
			Session session = Session.getDefaultInstance(props);
			MimeMessage msg = new MimeMessage(session);

			// Set contents of mail
			try {
				msg.setSubject(subject);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.setText(body);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.setFrom(new InternetAddress(username));
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.addRecipient(Message.RecipientType.TO, new InternetAddress(recipient));
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			// Mail sending handling
			Transport transport = null;
			try {
				transport = session.getTransport("smtps");
			} catch (NoSuchProviderException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.connect(host, username, password);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.sendMessage(msg, msg.getAllRecipients());
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.close();
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			jp.setVisible(false);
			Intro gui = new Intro();
			gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			gui.setSize(500, 300);
			gui.setLocationRelativeTo(null);

			gui.setVisible(true);
			gui.setResizable(false);

			gui.setTitle("IMPS Ver.1.0");
		} else if (ob == exit) {
			String pw_query = "select * from `keys` where `acnt_no` = " + id_num + "";

			StringBuffer keyBuff = new StringBuffer();
			String key = new String();
			String keySource = new String("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*?/");
			while (keyBuff.length() < 16) {
				Random r = new Random();
				int index = r.nextInt(keySource.length());
				keyBuff.append(keySource.charAt(index));
			}
			key = keyBuff.toString();

			Encryptor aes256 = null;
			try {
				aes256 = new Encryptor(key);
			} catch (UnsupportedEncodingException e4) {
				// TODO Auto-generated catch block
				e4.printStackTrace();
			}

			try {
				rs = st.executeQuery(pw_query);
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}

			try {
				if (st.execute(pw_query)) {
					rs = st.getResultSet();
				}
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}

			try {
				while (rs.next()) {
					String user_pw = rs.getString("pw_sequence");
					String text = new String(user_pw);
					String encText = null;
					try {
						encText = aes256.aesEncode(text);
					} catch (InvalidKeyException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (UnsupportedEncodingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (NoSuchAlgorithmException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (NoSuchPaddingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (InvalidAlgorithmParameterException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (IllegalBlockSizeException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					} catch (BadPaddingException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
					String update_query = "UPDATE `keys` SET `pw_sequence` = '" + encText + "' WHERE `acnt_no` = "
							+ id_num + " and `pw_sequence` = '" + user_pw + "'";

					st2.executeUpdate(update_query);
				}
			} catch (SQLException e3) {
				// TODO Auto-generated catch block
				e3.printStackTrace();
			}
			String sql2 = "select * from `account` where `no` = " + id_num + "";

			try {
				rs = st.executeQuery(sql2);
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			try {
				if (st.execute(sql2)) {
					rs = st.getResultSet();
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			String str = null;
			String user_name = null;

			try {
				while (rs.next()) {
					str = rs.getString("email");
					user_name = rs.getString("name");
				}
			} catch (SQLException e2) {
				// TODO Auto-generated catch block
				e2.printStackTrace();
			}

			// Mail configuration
			String host = "smtp.gmail.com";
			String username = "ku.mofteam@gmail.com";
			String password = "1q2w3e@@";

			// Set mail contents
			String recipient = "" + str + "";
			String subject = "Thanks for using our IPMS.";
			String body = "Dear " + user_name + "\n" + "Thanks for using our IPMS service.\n"
					+ "Your decryption key is " + key + "\n" + "Many thanks for your time";

			// Set properties
			Properties props = new Properties();
			props.put("mail.smtps.auth", "true");

			// Mail session
			Session session = Session.getDefaultInstance(props);
			MimeMessage msg = new MimeMessage(session);

			// Set mail contents
			try {
				msg.setSubject(subject);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.setText(body);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.setFrom(new InternetAddress(username));
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				msg.addRecipient(Message.RecipientType.TO, new InternetAddress(recipient));
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			// Mail send handling
			Transport transport = null;
			try {
				transport = session.getTransport("smtps");
			} catch (NoSuchProviderException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.connect(host, username, password);
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.sendMessage(msg, msg.getAllRecipients());
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			try {
				transport.close();
			} catch (MessagingException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}

			jp.setVisible(false);
		} else if (ob == info) {

			JOptionPane.showMessageDialog(helpMenu, "Copyright (C) Korea University Information Security MOF Team",
					"Info", JOptionPane.INFORMATION_MESSAGE);

		}
	}

	public String hash256(String str) {

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

	public void mouseClicked(MouseEvent e) {
		int srow = jt.getSelectedRow(); // row index
		Object name = jt.getValueAt(srow, 0);
		Object id = jt.getValueAt(srow, 1);
		Object pw = jt.getValueAt(srow, 2);

		label.setText(name + " - ID: " + id + ", PW: " + pw);

	}

	@Override
	public void mousePressed(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseReleased(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	public void fileSave() throws IOException {
		FileOutputStream output = new FileOutputStream("out.txt");
		int row = jt.getRowCount();
		int col = jt.getColumnCount();

		for (int i = 0; i < row; i++) {
			for (int j = 0; j < col; j++) {
				String data = (String) jt.getValueAt(i, j);
				output.write(data.getBytes());
				String d1 = " ";
				output.write(d1.getBytes());
			}
			String d2 = (String) "\n";
			output.write(d2.getBytes());
		}

		output.close();
	}

	@Override
	public void windowActivated(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowClosed(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowClosing(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowDeactivated(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowDeiconified(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowIconified(WindowEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void windowOpened(WindowEvent e) {
		// TODO Auto-generated method stub

	}

}
