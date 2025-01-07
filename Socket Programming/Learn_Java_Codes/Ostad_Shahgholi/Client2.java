/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication4;

import java.io.DataInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.nio.ByteBuffer;

/**
 *
 * @author Behrouz
 */
public class Client2 {
     public static void main(String[] args) {            
        try{            
          Socket s=new Socket(InetAddress.getByName("127.0.0.1"),2000);
          System.out.println(s.getLocalPort());                         
          OutputStream o=s.getOutputStream();
          InputStream in=s.getInputStream();
          DataInputStream din=new DataInputStream(in);
          PrintWriter p=new PrintWriter(o);
          
          p.println(">>hello\r\n");
          p.flush();                    
          System.out.println(din.readLine());              
        
          while (true);                            
        }catch(Exception e){
            e.printStackTrace();
        }
    }
}
