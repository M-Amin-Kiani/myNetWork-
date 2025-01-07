/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication4;
import java.net.InetSocketAddress;
import java.nio.ByteBuffer;
import java.nio.channels.*;
import java.util.Scanner;
import java.util.concurrent.Future;
/**
 *
 * @author Behrouz
 */
public class AsynchServer {
    public static void main(String[] arg){
       try{
        AsynchronousServerSocketChannel server = AsynchronousServerSocketChannel.open();
        server.bind(new InetSocketAddress("127.0.0.1", 2000));
        Future<AsynchronousSocketChannel> acceptFuture = server.accept();
        while (true){

            //do other work
            System.out.println("before get socket channel");
            AsynchronousSocketChannel clientChannel  = acceptFuture.get();
            System.out.println("after get socket channel");
            if ((clientChannel != null) && (clientChannel.isOpen())) {        
                ByteBuffer buffer = ByteBuffer.allocate(32);
                Future<Integer> readResult  = clientChannel.read(buffer);
                System.out.println("call for read done");
                //do other work
                readResult.get();
                System.out.println("read done: "+new String(buffer.array()).trim());             
                buffer.flip();
                Future<Integer> writeResult = clientChannel.write(buffer);
                System.out.println("call for write done");
                //do other work
                writeResult.get();
                System.out.println("write done");
                buffer.clear(); 
                clientChannel.close();
             }        
        }
      }catch (Exception e){
                e.printStackTrace();
      } 
}
}
