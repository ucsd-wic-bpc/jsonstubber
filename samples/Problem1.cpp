#include <iomanip>
#include <stdexcept>
#include <vector>
#include <cstdlib>
#include <utility>
#include <cstdarg>
#include <sstream>
#include <string>
#include <map>
#include <iostream>
#include <stack>

	
	int potateAndRoll(int hello) {
	
		//TODO
		return 0;
	
	}
	
	#ifndef JSON_OBJECT_HPP
	#define JSON_OBJECT_HPP
	
	
	class JSONObject {
	  private:
	    std::string data;
	
	  public:
	    JSONObject();
	    JSONObject(std::string data);
	
	    template <typename T>
	    T cast_data();
	
	    template <typename T>
	    std::pair<T*, int> cast_to_list();
	};
	
	template <> int JSONObject::cast_data() {
	  return atoi(this->data.c_str());
	}
	
	template <> double JSONObject::cast_data() {
	  return atof(this->data.c_str());
	}
	
	template <> char JSONObject::cast_data() {
	  return this->data[0];
	}
	
	template <> bool JSONObject::cast_data() {
	  return this->data == "true";
	}
	
	template <> std::string JSONObject::cast_data() {
	  return this->data;
	}
	
	#endif
	#ifndef JSON_LIST_HPP
	#define JSON_LIST_HPP
	
	
	
	class JSONList : public JSONObject {
	  private:
	    std::vector<JSONObject*> entries;
	    std::map<char, char> wrapCharacters;
	
	    bool is_delim_char(char c);
	    char get_closing_delim_from_stack(std::stack<char>& stack);
	    void populate_entries_from_string(std::string str);
	
	  public:
	    JSONList(std::string data);
	
	    JSONObject* get_item(int index);
	    int get_entry_count();
	
	    ~JSONList();
	};
	
	#endif
	#ifndef JSON_PARSER_HPP
	#define JSON_PARSER_HPP
	
	
	class JSONParser {
	  public:
	    static JSONObject* get_obj_from_str(std::string str);
	};
	
	#endif
	
	class Unifiedstr {
	  public:
	    template <typename T>
	    static std::string to_string(T obj);
	
	    template <typename T>
	    static std::string deep_to_string(void* arr, int depth, ...);
	
	  private:
	    template <typename T>
	    static std::string deep_to_string_stacked(void* arr, std::vector<int>& lengths, int curdepth=0);
	};
	
	template <typename T> std::string Unifiedstr::to_string(T obj) {
	  std::ostringstream convert;
	  convert << obj;
	  return convert.str();
	}
	
	template <> std::string Unifiedstr::to_string(bool obj) {
	  return obj ? "True" : "False";
	}
	
	template <> std::string Unifiedstr::to_string(double obj) {
	  std::ostringstream convert;
	  convert << std::setprecision(1) << std::fixed;
	  convert << obj;
	  return convert.str();
	}
	
	template <typename T>
	std::string Unifiedstr::deep_to_string(void* arr, int depth, ...) {
	  std::vector<int> lengths_vec;
	
	  va_list lengths;
	  va_start(lengths, depth);
	  for (int i = 0; i < depth; i++) {
	    lengths_vec.push_back(va_arg(lengths, int));
	  }
	  va_end(lengths);
	
	  return Unifiedstr::deep_to_string_stacked<T>(arr, lengths_vec);
	}
	
	template <typename T>
	std::string Unifiedstr::deep_to_string_stacked(void* arr, std::vector<int>& lengths, int curdepth) {
	  if (lengths.size() == 0)
	    return "";
	
	  std::ostringstream write;
	  write << "[";
	
	  int length = lengths[curdepth];
	  for (int i = 0; i < length; i++) {
	    if (curdepth >= (lengths.size() - 1)) {
	      write << Unifiedstr::to_string(((T*)arr)[i]);
	    }
	    else {
	      int inner_length = lengths[curdepth+1];
	      T* t_ptr = (T*) arr;
	      T* inner_array = (t_ptr + (inner_length * i));
	      write << Unifiedstr::deep_to_string_stacked<T>((void*)inner_array, lengths, curdepth+1);
	    }
	
	    if (i < (length - 1))
	      write << ", ";
	  }
	
	  write << "]";
	
	  return write.str();
	}
	int main() {
		std::string inputContents;
		getline(std::cin, inputContents);
		JSONList* argList = (JSONList*) JSONParser::get_obj_from_str(inputContents);
		
		int hello = argList->get_item(0)->cast_data<int>();
		
		int output = potateAndRoll(hello);
		std::cout << Unifiedstr::to_string(output) << std::endl;
	
	}

JSONList::JSONList(std::string data) {
  this->wrapCharacters['['] = ']';
  this->wrapCharacters['"'] = '"';
  this->populate_entries_from_string(data);
}

JSONObject* JSONList::get_item(int index) {
  return this->entries.at(index);
}

int JSONList::get_entry_count() {
  return this->entries.size();
}

JSONList::~JSONList() {
  std::vector<JSONObject*>::iterator it;
  for (it = this->entries.begin(); it != this->entries.end(); it++)
    delete(*it);
}

bool JSONList::is_delim_char(char c) {
  try {
    char temp = this->wrapCharacters.at(c);
  } 
  catch (const std::out_of_range& oor) {
    return false;
  }
  return true;
}

char JSONList::get_closing_delim_from_stack(std::stack<char>& stack) {
  return this->wrapCharacters.at(stack.top());
}

void JSONList::populate_entries_from_string(std::string str) {
  std::stack<char> delimiter_stack;
  std::string current_string;

  for (int i = 0; i < str.length(); ++i) {
    if (!delimiter_stack.empty() && 
        str[i] == get_closing_delim_from_stack(delimiter_stack))
      delimiter_stack.pop();
    else if (is_delim_char(str[i]))
      delimiter_stack.push(str[i]);

    // Check to see if we have reached a comma
    if ((str[i] == ',' || i == str.length() - 1) && delimiter_stack.empty()) {
      // Check if last item
      if (i == str.length() - 1) current_string.push_back(str[i]);
      this->entries.push_back(JSONParser::get_obj_from_str(current_string));
      current_string.erase(0, std::string::npos);
      continue;
    }
    current_string.push_back(str[i]);
  }
}

JSONObject::JSONObject() {
  this->data = "";
}

JSONObject::JSONObject(std::string data) {
  this->data = data;
}

template <typename T>
std::pair<T*, int> JSONObject::cast_to_list() {
  JSONList* thisList = (JSONList*) this;
  int len = thisList->get_entry_count();
  T* arr = new T[len];
  for (int ii = 0; ii < len; ii++)
    arr[ii] = thisList->get_item(ii)->cast_data<T>();
  return std::make_pair(arr, len);
}

JSONObject* JSONParser::get_obj_from_str(std::string str) {
    // Check if surrounded by quotes, list brackets, or nothing
    if (str[0] == '[' && str[str.length() - 1] == ']')
      return new JSONList(str.substr(1, str.length() - 2));
    else if (str[0] == '"' && str[str.length() - 1] == '"')
      return new JSONObject(str.substr(1, str.length() - 2));
    else
      return new JSONObject(str);
}
