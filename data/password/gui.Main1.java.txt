import java.awt.Component;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.InputEvent;
import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;

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
import javax.swing.KeyStroke;
import javax.swing.table.DefaultTableModel;

public class Main1 extends Intro implements MouseListener, ActionListener {
	JFrame jp = new JFrame("IPMS");
	JTable jt;
	JComboBox box;
	DefaultTableModel dtm;
	InputForm form;
	SearchForm form_search;
	EditMasterForm form_master;
	EditEmailForm form_email;
	DeactivateForm form_deactivate;

	int srow;
	JMenuBar menuBar = new JMenuBar();
	JMenu mainMenu = new JMenu("Menu");
	JMenu helpMenu = new JMenu("Help");
	JMenuItem editMaster = new JMenuItem("Edit master password");

	JMenuItem editEmail = new JMenuItem("Edit master email");
	JMenuItem Deactivate = new JMenuItem("Account Setting");

	JMenuItem logOut = new JMenuItem("Log Out");
	JMenuItem exit = new JMenuItem("Exit");
	JMenuItem version = new JMenuItem("Version");
	JMenuItem info = new JMenuItem("Info");
	JScrollPane scroll;
	JLabel label, label_info;
	JPanel northp,southp;
	JButton bt_add, bt_del, bt_up, bt_search; 	
	Object[][] rowData={
			{"Naver", "test","testtest", "http://www.naver.com/"},
			{"BlackBoard", "black","fortest", "http://kulms.korea.ac.kr/"},
			{"Daum", "daumdaum","daumtest", "http://www.daum.net/"}
	};
	
	Object[] columnNames={"Name", "ID", "Password", "link"};

	public Main1() {
		form = new InputForm();
		form_search = new SearchForm();
		form_deactivate = new DeactivateForm();
		form_email = new EditEmailForm();
		form_master = new EditMasterForm();
		box = form_search.box;
		 
		dtm = new DefaultTableModel(rowData, columnNames);
		jt=new JTable (dtm);
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
		 
		 
		jp.add("Center",scroll);
		jp.add("North",northp);
		jp.add("South",southp);
		jp.setBounds(400,300,300,300);
		jp.setSize(1000, 700);
		jp.setVisible(true);

		eventUp();

		//create menu
		mainMenu.add(Deactivate);
		mainMenu.add(editEmail);
		mainMenu.add(editMaster);
		mainMenu.addSeparator(); //separator
		
		mainMenu.add(logOut);
		mainMenu.addSeparator();
		mainMenu.add(exit);
		helpMenu.add(info);

		//add menu to menubar
		menuBar.add(mainMenu);
		menuBar.add(helpMenu);

		//add menubar
		jp.setJMenuBar(menuBar);
		
	    jp.setLocationRelativeTo(null);
	    jp.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
	}

	//action handling
	private void eventUp(){
	    jt.addMouseListener(this);
	    
	    mainMenu.addActionListener(this);
	    helpMenu.addActionListener(this);
	    bt_add.addActionListener(this);
	    bt_del.addActionListener(this);
	    bt_up.addActionListener(this);
	    bt_search.addActionListener(this);
	    
	    form.bt_input.addActionListener(this);
	    form.bt_cancel.addActionListener(this);
	    
	    form_search.bt_input.addActionListener(this);
	    form_search.bt_cancel.addActionListener(this);
	    
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

		Object ob=e.getSource();
		if(ob==bt_add){		//add button
			form.initTF();
			form.setVisible(true);
		}
		//input button (insert / edit)
		else if(ob==form.bt_input){		
			String name= form.tf_name.getText();
			String id= form.tf_id.getText();
			String pw= form.tf_pw.getText();
			String link= form.tf_link.getText();
		      
			//check null - if there is no input in any of the fields, do not accept	
			if(name == null  || name.length() == 0){
				JOptionPane.showMessageDialog(form, "Input name!!"); 
				form.tf_name.requestFocus();
				return;
			}
		      	//alert message for any empty input
			if(id.length()==0){
				JOptionPane.showMessageDialog(form, "Input ID!!"); 
				form.tf_id.requestFocus();
				return;
			}
		      
			if(pw.length()==0){
				JOptionPane.showMessageDialog(form, "Input password!!");
				form.tf_pw.requestFocus();
				return;
			}
			
			if(link.length()==0){
				JOptionPane.showMessageDialog(form, "Input link!!");
				form.tf_link.requestFocus();
				return;
			}
			
			if(form.strength.getValue()<20){
				JOptionPane.showMessageDialog(form, "Password is too weak!!");
				form.tf_pw.requestFocus();
				return;
			}
			//add new form
			if(form.getTitle().equals("Add new")){		
				Object rowData[] = {name, id, pw, link};
				dtm.addRow(rowData);
				try {
					fileSave();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}

			}
			else {	//edit form
				jt.setValueAt(name, srow, 0);	//edit name
				jt.setValueAt(id, srow, 1);		//edit id
				jt.setValueAt(pw, srow, 2);		//edit pw
				jt.setValueAt(link, srow, 3);	//edit link
				try {
					fileSave();
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
			}
			form.setVisible(false);
			jp.setVisible(true);
		}
		//cancel button
		else if(ob==form.bt_cancel){
			form.setVisible(false);
			jp.setVisible(true);
		}
		//delete button
		else if(ob==bt_del){	
			srow = jt.getSelectedRow();
			if(srow==-1){
				JOptionPane.showMessageDialog(jp,"Select row to delete!!");
				return;
			}
			String name = (String) jt.getValueAt(srow,0);
			String id  = (String) jt.getValueAt(srow,1);
			String pw  = (String) jt.getValueAt(srow,2);
			String link  = (String) jt.getValueAt(srow,3);
			//delete from the table
			for(int i=0; i<jt.getRowCount(); i++){
				if(name.equals(jt.getValueAt(i,0)) && id.equals(jt.getValueAt(i, 1)) && pw.equals(jt.getValueAt(i, 2)) && link.equals(jt.getValueAt(i,3))){
					dtm.removeRow(i);
				}
			}
			try {
				fileSave();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}
		else if(ob==bt_up){		//edit button
			srow = jt.getSelectedRow(); 
     
			if(srow==-1){		//if unselected, srow value is -1
				JOptionPane.showMessageDialog(jp, "Select row to edit!!");
				return;
			}
		     
			String name = (String) jt.getValueAt(srow,0);
			String id  = (String) jt.getValueAt(srow,1);
			String pw  = (String) jt.getValueAt(srow,2);
			String link  = (String) jt.getValueAt(srow,3);
			
			form.tf_name.setText(name);
			form.tf_id.setText(id);
			form.tf_pw.setText(pw);
			form.tf_link.setText(link);
			form.initUp();
			form.setVisible(true);
		}
		else if(ob==bt_search){		//search button
		     
			String tf  = form_search.tf.getText();
			
			form_search.tf.setText(tf);
			form_search.initSearch();
			form_search.setVisible(true);
		}
		else if(ob==form_search.bt_input) {
			String input = form_search.tf.getText();
			
			if(input == null  || input.length() == 0){
			      //check nullable
					JOptionPane.showMessageDialog(form, "Input anything please!!"); 
					form_search.tf.requestFocus();
					return;
				}
			else
			{
				if(box.getSelectedItem() == "Name")
				{
					for(int i = 0; i < rowData.length; i++)
					{
						if(input.compareTo((String)rowData[i][0]) == 0)
						{
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(false);
					jp.setVisible(true);
				}
				else if(box.getSelectedItem() == "ID")
				{
					for(int i = 0; i < rowData.length; i++)
					{
						if(input.compareTo((String)rowData[i][1]) == 0)
						{
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(true);
					jp.setVisible(true);
				}
				else if(box.getSelectedItem() == "Password")
				{
					for(int i = 0; i < rowData.length; i++)
					{
						if(input.compareTo((String)rowData[i][2]) == 0)
						{
							form_search.setVisible(false);
							jp.setVisible(true);
							jt.setRowSelectionInterval(i, i);
							return;
						}
					}
					form_search.setVisible(false);
					jp.setVisible(true);
				}
				else
				{
					for(int i = 0; i < rowData.length; i++)
					{
						if(input.compareTo((String)rowData[i][3]) == 0 || ((String) rowData[i][3]).contains(input))
						{
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
			
		}
		else if(ob==form_search.bt_cancel){
			form_search.setVisible(false);
			jp.setVisible(true);
		}

		else if(ob==editMaster) {
			form_master.initEditMaster();
			form_master.setVisible(true);
		}
		else if(ob==form_master.bt_input){
			String pw= form_master.tf_pw.getText();
			String confirm= form_master.tf_confirm.getText();

			//check null - if there is no input in any of the fields, do not accept	
			if(pw == null  || pw.length() == 0){
				JOptionPane.showMessageDialog(form_master, "Input New Password!!"); 
				form_master.tf_pw.requestFocus();
				return;
			}
		      
			if(confirm.length()==0){
				JOptionPane.showMessageDialog(form_master, "Confirm New Password!!"); 
				form_master.tf_confirm.requestFocus();
				return;
			}
			
			if(confirm.equals(pw) == false)
			{
				JOptionPane.showMessageDialog(form_master, "Password not Confirmed properly! Try Again!!"); 
				form_master.tf_confirm.requestFocus();
				return;
			}
			
			form_master.setVisible(false);
			jp.setVisible(true);
		}
		else if(ob==form_master.bt_cancel){
			form_master.setVisible(false);
			jp.setVisible(true);
		}
		else if(ob==logOut){
			jp.setVisible(false);
			Intro gui =new Intro();
			gui.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			gui.setSize(500,300);
			gui.setLocationRelativeTo(null);

			gui.setVisible(true);
			gui.setResizable(false);

			gui.setTitle("IMPS Ver.1.0");
		}
		else if (ob == Deactivate) {
			form_deactivate.initDeactivate();
			form_deactivate.setVisible(true);
		} 
		else if (ob == editEmail) {
			form_email.initEditEmail();
			form_email.setVisible(true);
		} 
		else if (ob == editMaster) {
			form_master.initEditMaster();
			form_master.setVisible(true);
		} 
		else if(ob==exit){
			jp.setVisible(false);
		}
		else if(ob==info){	
			JOptionPane.showMessageDialog(helpMenu, "Copyright (C) Korea University Information Security MOF Team", "Info", JOptionPane.INFORMATION_MESSAGE);
		}
	}

	 public void mouseClicked(MouseEvent e) {
	     int srow= jt.getSelectedRow();		//row index
	     Object name=jt.getValueAt(srow, 0);
	     Object id=jt.getValueAt(srow, 1);
	     Object pw=jt.getValueAt(srow, 2);
	     
	     label.setText(name+" - ID: "+id+", PW: "+pw);
	     
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
	        int row=jt.getRowCount();
	        int col=jt.getColumnCount();
	        
	        for(int i=0; i<row; i++) {
	        	for(int j=0;j<col;j++){
	        		String data=(String) jt.getValueAt(i, j);
	        		output.write(data.getBytes());
	        		String d1=" ";
	        		output.write(d1.getBytes());
	        	}
	        	String d2=(String)"\n";
	        	output.write(d2.getBytes());
	        }

	        output.close();

	 }

}
