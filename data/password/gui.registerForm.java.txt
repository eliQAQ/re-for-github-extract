import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;


public class registerForm extends JFrame{
 
	 JLabel la_id, la_pw, la_confirm;
	 JTextField tf_id;
	 JTextField tf_pw, tf_confirm;
	 JButton bt_input, bt_cancel;
	
	 public registerForm() {
		
	  setTitle("Register");
	  la_id = new JLabel("ID");
	  la_pw = new JLabel("Master password");
	  la_confirm = new JLabel ("Confirm");
	  
	  tf_id = new JTextField();
	  tf_pw = new JTextField();
	  tf_confirm = new JTextField();
	  
	  bt_input = new JButton("OK");
	  bt_cancel = new JButton("Cancel");
	 
	  setLayout(null);
	  
	  //Component setting
	  la_id.setBounds(30, 30, 120, 30);
	  la_pw.setBounds(30, 70, 120, 30);
	  la_confirm.setBounds(30,110,120,30);
	  
	  tf_id.setBounds(160, 30, 120, 30);
	  tf_pw.setBounds(160, 70, 120, 30);
	  tf_confirm.setBounds(160,110,120,30);
	  
	  bt_input.setBounds(80, 200, 60, 30);
	  bt_cancel.setBounds(150, 200, 100, 30);
	  
	  //Component addition
	  add(la_id);
	  add(la_pw);
	  add(la_confirm);
	
	  add(tf_id);
	  add(tf_pw);
	  add(tf_confirm);
	
	  add(bt_input);  
	  add(bt_cancel);
	        
	  bt_input.addActionListener(new ActionListener (){
		  public void actionPerformed(ActionEvent e) {
			  String id = tf_id.getText();
			  String pw = tf_pw.getText();
			  String confirm = tf_confirm.getText();
			  
			  if(id.length() == 0)
			  {
				  JOptionPane.showMessageDialog(null, "Input name!!"); 
				  return;
			  }
			  else if(pw.length() == 0)
			  {
				  JOptionPane.showMessageDialog(null, "Input password!!"); 
				  return;
			  }
			  else if(confirm.length() == 0)
			  {
				  JOptionPane.showMessageDialog(null, "Confirm your password!!"); 
				  return;
			  }
			  
				setVisible(false);
		  }
	  });
	  
	  bt_cancel.addActionListener(new ActionListener (){
		  public void actionPerformed(ActionEvent e) {
				setVisible(false);
		  }
	  });
	    
	  setBounds(0, 0, 330, 300);
	  setLocationRelativeTo(null);
	
	  setResizable(false);  //fix frame size
	  setVisible(true);

	 }
	
		
 } 
