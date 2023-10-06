import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JTextField;
import javax.swing.event.ChangeListener;

public class EditMasterForm extends JFrame {
	JLabel la_box, la_box2;
	JTextField tf_pw, tf_confirm;
	JButton bt_input, bt_cancel;
	ChangeListener listener;
	 
	public EditMasterForm() {

		setTitle("Edit Master password");
		  
		la_box = new JLabel ("Edit Password");
		la_box2 = new JLabel ("Confirm Password");
		  
		tf_pw = new JTextField();
		tf_confirm = new JTextField();
		  
		bt_input = new JButton("OK");
		bt_cancel = new JButton("Cancel");
		 
		setLayout(null);
		
		//Component setting and addition
		la_box.setBounds(30, 30, 120, 30);
		tf_pw.setBounds(30, 80 , 250, 30);
		la_box2.setBounds(30, 120, 120, 30);
		tf_confirm.setBounds(30, 160, 250, 30);
		bt_input.setBounds(30, 300, 60, 30);
		bt_cancel.setBounds(100, 300, 120, 30);
	  
		add(la_box);
		add(la_box2);
		add(tf_pw);
		add(tf_confirm);
		add(bt_input);  
		add(bt_cancel);
		        
		setBounds(500, 500, 400, 400);
		setLocationRelativeTo(null);

		setResizable(false);    
	 }
	 
	//Edit master password form
	public void initEditMaster(){
		setTitle("Edit Master password");

		tf_pw.setText("");
		tf_confirm.setText("");
		tf_pw.requestFocus();
	}
}
