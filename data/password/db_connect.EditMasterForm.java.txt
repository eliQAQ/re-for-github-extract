package db_connec_test;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.event.ChangeListener;

@SuppressWarnings("serial")
public class EditMasterForm extends JFrame {
	JLabel la_box, la_box2, la_box0;
	JTextField tf_pw, tf_confirm, tf_current;
	JButton bt_input, bt_cancel;
	ChangeListener listener;

	public EditMasterForm() {
		// Set UI components
		setTitle("Edit Master password");

		la_box0 = new JLabel("Current Password");
		la_box = new JLabel("Edit Password");
		la_box2 = new JLabel("Confirm Password");

		tf_current = new JPasswordField();
		tf_pw = new JPasswordField();
		tf_confirm = new JPasswordField();

		bt_input = new JButton("OK");
		bt_cancel = new JButton("Cancel");
		setLayout(null);

		// Component setting and addition
		la_box0.setBounds(30, 30, 120, 30);
		tf_current.setBounds(30, 60, 250, 30);

		la_box.setBounds(30, 100, 120, 30);
		tf_pw.setBounds(30, 130, 250, 30);

		la_box2.setBounds(30, 160, 120, 30);
		tf_confirm.setBounds(30, 190, 250, 30);

		bt_input.setBounds(30, 300, 60, 30);
		bt_cancel.setBounds(100, 300, 120, 30);

		// Create components
		add(la_box0);
		add(la_box);
		add(la_box2);
		add(tf_current);
		add(tf_pw);
		add(tf_confirm);
		add(bt_input);
		add(bt_cancel);

		setBounds(500, 500, 400, 400);
		setResizable(false);
	}

	// Edit master password form
	public void initEditMaster() {
		setTitle("Edit Master password");

		tf_pw.setText("");
		tf_confirm.setText("");
		tf_pw.requestFocus();
	}
}
