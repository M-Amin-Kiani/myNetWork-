/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package javaapplication4;
import java.net.*;
import java.io.*;

/**
 *
 * @author Behrouz
 */

public class Client {
 static class Test1 implements Test{
        private int t;
        public Test1(int i)
        {
            t=i;
        }
        public void print(){
            System.out.println("Test Value: "+t);
        }
 };    
    public static void main(String[] args) {            
        try{            
          Socket s=new Socket(InetAddress.getByName("127.0.0.1"),2000);          
          System.out.println(s.getLocalPort());
          DataInputStream in=new DataInputStream(s.getInputStream());
          System.out.println(in.readInt());
         
          OutputStream o=s.getOutputStream();
          PrintWriter p=new PrintWriter(o);
          p.println("P1ertretetettretqwq2eytyy");
          p.flush();                                
          Test1  t= new Test1(100);          
          ObjectOutputStream oos=new ObjectOutputStream(o);
          oos.writeObject(t);
          oos.flush();                            
          while(true);                    
        }catch(Exception e){
            e.printStackTrace();
        }
    }

}
