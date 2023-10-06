
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.event.ChangeListener;

/*
 * Deactivate form for deactivate user account
 */
@SuppressWarnings("serial")
public class DeactivateForm extends JFrame {
	JLabel la_box, la_box2;
	JTextField tf_pw, tf_confirm;
	JButton bt_input, bt_cancel;
	ChangeListener listener;

	public DeactivateForm() {

		setTitle("Deactivate your ID");

		la_box = new JLabel("Your Password");
		la_box2 = new JLabel("Confirm Password");

		tf_pw = new JPasswordField();
		tf_confirm = new JPasswordField();

		bt_input = new JButton("OK");
		bt_cancel = new JButton("Cancel");

		setLayout(null);

		// Component setting and addition
		la_box.setBounds(30, 30, 120, 30);
		tf_pw.setBounds(30, 60, 250, 30);

		la_box2.setBounds(30, 100, 120, 30);
		tf_confirm.setBounds(30, 130, 250, 30);

		bt_input.setBounds(30, 200, 60, 30);
		bt_cancel.setBounds(100, 200, 120, 30);

		add(la_box);
		add(la_box2);
		add(tf_pw);
		add(tf_confirm);
		add(bt_input);
		add(bt_cancel);

		setBounds(200, 200, 400, 300);
		setLocationRelativeTo(null);

		setResizable(false);
	}

	// Deactivate the user account form
	public void initDeactivate() {
		setTitle("Deactivate your ID");

		tf_pw.setText("");
		tf_confirm.setText("");
		tf_pw.requestFocus();
	}
}
