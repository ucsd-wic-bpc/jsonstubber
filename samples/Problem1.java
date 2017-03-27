import java.util.ArrayList;
import java.util.Stack;
import java.util.Dictionary;
import java.util.Hashtable;
import java.util.Arrays;
import java.util.Scanner;

public class Problem1 {

	
	public static int potateAndRoll(int hello) {
		//TODO
		return 0;
	
	}
	
	
	public static void main(String[] args) {
		String input = new Scanner(System.in).nextLine();
		JSONList argList = (JSONList) JSONParser.getObjectFromString(input);
		
		int hello = argList.getItem(0).castToInt();
		
		int output = potateAndRoll(hello);
		System.out.println(Unifiedstr.toString(output));
	
	}
}
/*
 * jsonFASTParse
 * @author: Brandon Milton
 * http://brandonio21.com
 *
 * A small Java library meant to parse JSON in a quick fashion, given that the
 * end-user is aware of the JSON data schema. Does not support dictionaries.
 */

class JSONList extends JSONObject {
  public ArrayList<JSONObject> entries;
  private  Dictionary<Character, Character> wrapCharacters;

  public JSONList(String data) {
    this.entries = new ArrayList<JSONObject>();
    this.wrapCharacters = new Hashtable<Character, Character>();
    wrapCharacters.put('[', ']');
    wrapCharacters.put('"', '"');
    this.populateEntriesFromString(data);
  }

  public int getEntryCount() {
    return this.entries.size();
  }

  public JSONObject getItem(int index) {
    return this.entries.get(index);
  }

  private void populateEntriesFromString(String str) {
    Stack<Character> delimiterStack = new Stack<Character>();
    StringBuilder currentString = new StringBuilder();

    for (int i = 0; i < str.length(); i++) {
      if (!delimiterStack.empty() && str.charAt(i) == getClosingDelimFromStack(delimiterStack))
        delimiterStack.pop();
      else if (isDelimiterCharacter(str.charAt(i)))
        delimiterStack.push(str.charAt(i));

      // Check to see if we have reached a comma
      if ((str.charAt(i) == ',' || i == str.length() - 1) && delimiterStack.empty()) {
        // Check if last item
        if (i == str.length() - 1) currentString.append(str.charAt(i));
        this.entries.add(JSONParser.getObjectFromString(currentString.toString()));
        currentString.delete(0, currentString.length());
        continue;
      }
      currentString.append(str.charAt(i));
    }
  }

  private boolean isDelimiterCharacter(char c) {
    return this.wrapCharacters.get(c) != null;
  }

  private char getClosingDelimFromStack(Stack<Character> stack) {
    return this.wrapCharacters.get(stack.peek());
  }
}
/*
 * jsonFASTParse
 * @author: Brandon Milton
 * http://brandonio21.com
 *
 * A small Java library meant to parse JSON in a quick fashion, given that the
 * end-user is aware of the JSON data schema. Does not support dictionaries.
 */

class JSONObject {
  private String data;

  public JSONObject() {
    this.data = "";
  }

  public JSONObject(String data) {
    this.data = data;
  }

  public String getData() {
    return this.data;
  }

  public String castToString() {
    return this.data;
  }

  public int castToInt() {
    return Integer.parseInt(this.data);
  }

  public double castToDouble() {
    return Double.parseDouble(this.data);
  }

  public char castToChar() {
    return this.data.charAt(0);
  }

  public boolean castToBool() {
    return Boolean.parseBoolean(this.data);
  }

}

/*
 * jsonFASTParse
 * @author: Brandon Milton
 * http://brandonio21.com
 *
 * A small Java library meant to parse JSON in a quick fashion, given that the
 * end-user is aware of the JSON data schema. Does not support dictionaries.
 */

class JSONParser {

  public static JSONObject getObjectFromString(String str) {
    // Check if surrounded by quotes, list brackets, or nothing
    if (str.charAt(0) == '[' && str.charAt(str.length() - 1) == ']')
      return new JSONList(str.substring(1, str.length() - 1));
    else if (str.charAt(0) == '"' && str.charAt(str.length() - 1) == '"')
      return new JSONObject(str.substring(1, str.length() - 1));
    else
      return new JSONObject(str);
  }

}


class Unifiedstr {

  public static String toString(boolean b) {
    return b ? "True" : "False";
  }

  public static String toString(boolean[] b) {
    String[] string_arr = new String[b.length];
    for (int i = 0; i < b.length; i++) {
      string_arr[i] = toString(b[i]);
    }
    
    return Arrays.toString(string_arr);
  }

  public static String toString(double d) {
    return String.valueOf(d);
  }

  public static String toString(double[] b) {
    String[] string_arr = new String[b.length];
    for (int i = 0; i < b.length; i++) {
      string_arr[i] = toString(b[i]);
    }
    
    return Arrays.toString(string_arr);
  }

  public static String toString(String s) {
    return s;
  }

  public static String toString(String[] b) {
    String[] string_arr = new String[b.length];
    for (int i = 0; i < b.length; i++) {
      string_arr[i] = toString(b[i]);
    }
    
    return Arrays.toString(string_arr);
  }

  public static String toString(char c) {
    return Character.toString(c);
  }

  public static String toString(char[] b) {
    String[] string_arr = new String[b.length];
    for (int i = 0; i < b.length; i++) {
      string_arr[i] = toString(b[i]);
    }
    
    return Arrays.toString(string_arr);
  }

  public static String toString(int i) {
    return Integer.toString(i);
  }

  public static String toString(int[] b) {
    String[] string_arr = new String[b.length];
    for (int i = 0; i < b.length; i++) {
      string_arr[i] = toString(b[i]);
    }
    
    return Arrays.toString(string_arr);
  }

  public static String deepToString(Object[] o) {
    StringBuilder buf = new StringBuilder();
    if (o == null) {
      return "null";
    }

    int index_max = o.length - 1;
    if (o.length == 0) {
      return "[]";
    }

    buf.append('[');

    for (int i = 0; i < o.length; i++) {
      Object element = o[i];
      if (element == null) {
        buf.append("null");
      } else {
        Class element_class = element.getClass();
        if (element_class == boolean.class)
          buf.append(toString((boolean) element));
        else if (element_class == double.class)
          buf.append(toString((double) element));
        else if (element_class == char.class)
          buf.append(toString((char) element));
        else if (element_class == int.class)
          buf.append(toString((int) element));
        else if (element_class == String.class)
          buf.append(toString((String) element));
        else if (element_class == boolean[].class)
          buf.append(toString((boolean[]) element));
        else if (element_class == double[].class)
          buf.append(toString((double[]) element));
        else if (element_class == char[].class)
          buf.append(toString((char[]) element));
        else if (element_class == int[].class)
          buf.append(toString((int[]) element));
        else if (element_class == String[].class)
          buf.append(toString((String[]) element));
      }

      if (i == index_max) 
        break;
      buf.append(", ");
    }
    buf.append(']');
    return buf.toString();
  }
}
